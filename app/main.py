import argparse
from pathlib import Path

from infrastructure.ifc_reader import load_ifc_elements
from infrastructure.console_writer import write_console_report
from infrastructure.json_writer import write_json_report
from infrastructure.csv_writer import write_csv_report
from infrastructure.sqlite_writer import (
write_sqlite_report,
query_issue_summary_latest,
query_issues_by_class_latest,
)

from core.auditor import run_audit as run_core_audit

def parse_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="IFC Model Auditor CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    # audit
    audit_parser = subparsers.add_parser(
        "audit",
        help="Run anaudit on an IFC file"
    )
    audit_parser.add_argument(
        "ifc_file",
        help="Path to the IFC file"
    )
    audit_parser.add_argument(
        "--output",
        default="output",
        help="Output directory for reports (default: output)"
    )

    audit_parser.add_argument(
        "--no-console",
        action="store_true",
        help="Disable console report output"
    )

    audit_parser.add_argument(
        "--no-json",
        action="store_true",
        help="Disable JSON report output"
    )

    audit_parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Disable CSV report output"
    )

    audit_parser.add_argument(
        "--no-sqlite",
        action="store_true",
        help="Disable SQLite report output"
    )

    # query
    query_parser = subparsers.add_parser(
        "query",
        help="Query the SQLite audit databse"
    )

    query_parser.add_argument(
        "--output",
        default="output",
        help="Output directory containing dubit.db (default: output)"
    )

    query_group = query_parser.add_mutually_exclusive_group()
    query_group.add_argument(
        "--issue-summary",
        action="store_true",
        help="Show issue counts grouped by issue code"
    )

    query_group.add_argument(
        "--issue-by-class",
        action="store_true",
        help="Show issue counts grouped by IFC class"
    )

    return parser

def print_issue_summary(rows: list[dict]) -> None:
    print("Issue Sumamry")
    print("-" * 40)

    if not rows:
        print("No issues found.")
        return
    for row in rows:
        print(f"{row['issue_code']}: {row['total']}")

def print_issue_by_class(rows: list[dict]) -> None:
    print("Issue by IFC Class")
    print("-" * 40)

    if not rows:
        print("No issues found.")
        return
    
    for row in rows:
        print(f"{row['ifc_class']: {row['total']}}")

def run_audit(args) -> None:
    ifc_path = Path(args.ifc_file)
    output_dir = Path(args.output)
    
    if not ifc_path.exists():
        raise FileNotFoundError(f"IFC file not found at: {ifc_path}")
    
    print (f"Reading IFC file: {ifc_path}")
    elements = load_ifc_elements(str(ifc_path))
    print(f"Loaded {len(elements)} elements")
    
    report = run_core_audit(elements, source_file=str(ifc_path))
    print(f"Audit complete: {report.total_elements} elements, {report.total_issues} issues")
    
    if not args.no_console:
        write_console_report(report)
    
    if not args.no_json:
        write_json_report(report, str(output_dir / "audit_report.json"))
                          
    if not args.no_csv:
        write_csv_report(report, str(output_dir))
    
    if not args.no_sqlite:
        write_sqlite_report(report, output_dir)
        
    print(f"Outputs writtent to {output_dir}")


def run_query(args) -> None:
    output_dir = Path(args.output)

    if args.issue_summary:
        rows = query_issue_summary_latest(output_dir)
        print_issue_summary(rows)
        return

    if args.issue_by_class:
        rows = query_issue_summary_latest(output_dir)
        print_issue_by_class(rows)
        return

    print("No query option selected. Use --issue-summary or --issue-by-class.")

def main() -> None:
    parser = parse_arguments()
    args = parser.parse_args()

    if args.command == "audit":
        run_audit(args)
    elif args.command == "query":
        run_query(args)
    else:
        parser.print_help()
    
if __name__ == "__main__":
    main()