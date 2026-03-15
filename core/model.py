from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ElementInfo:
    global_id: str
    ifc_class: str
    name: str | None

@dataclass
class IssueRecord:
    issue_code: str
    message: str
    global_id: str
    ifc_class: str
    element_name: str | None

@dataclass
class AuditReport:
    source_file: str
    total_elements: int
    counts_by_class: Dict[str, int]
    total_issues: int
    issues: List[IssueRecord]