from infrastructure.ifc_reader import load_ifc_elements
from core.auditor import run_audit

def main():
    source_file = "samples/test.ifc"

    elements = load_ifc_elements(source_file)

    report = run_audit(elements, source_file)

    print(f"Source file: {report.source_file}")
    print(f"Total elements: {report.total_elements}")
    print(f"Total issues: {report.total_issues}")

    print("\nCounts by class:")
    for ifc_class, count in report.counts_by_class.items():
        print(f"    {ifc_class}: {count}")
    
    print("\n First 10 issues:")
    for issue in report.issues[:10]:
        print(issue)

if __name__ == "__main__":
    main()