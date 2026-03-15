from infrastructure.ifc_reader import load_ifc_elements
from infrastructure.console_writer import write_console_report
from core.auditor import run_audit

def main():
    source_file = "samples/test.ifc"

    elements = load_ifc_elements(source_file)
    report = run_audit(elements, source_file)

    write_console_report(report)

    
if __name__ == "__main__":
    main()