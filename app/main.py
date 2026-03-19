import argparse

from infrastructure.ifc_reader import load_ifc_elements
from infrastructure.console_writer import write_console_report
from infrastructure.json_writer import write_json_report
from infrastructure.csv_writer import write_csv_report
from infrastructure.sqlite_writer import write_sqlite_report
from core.auditor import run_audit

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="IFC Model Auditor - lightweight IFC inspection tool"
    )

    parser.add_argument(
        "ifc_file",
        help="Path to the IFC file to analyze"
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Output directory for reports (default: output)"
    )

    parser.add_argument(
        "--no-console",
        action="store_true",
        help="Disable console report output"
    )

    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Disable JSON report output"
    )

    parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Disable CSV report output"
    )

    parser.add_argument(
        "--no-sqlite",
        action="store_true",
        help="Disable SQLite report output"
    )

    return parser.parse_args()

def main() -> None:

    args = parse_arguments()

    elements = load_ifc_elements(args.ifc_file)
    report = run_audit(elements, args.ifc_file)

    if not args.no_console:
        write_console_report(report)
    
    if not args.no_json:
        write_json_report(report, f"{args.output}/audit_report.json")
        print(f"JSON report written to {args.output}/audit_report.json")
    
    if not args.no_csv:
        write_csv_report(report, args.output)
        print(f"CSV report written to: {args.output}")
    
    if not args.no_sqlite:
        db_path = write_sqlite_report(report, args.output)
        print(f"SQLite report written to {args.output}")
    
if __name__ == "__main__":
    main()