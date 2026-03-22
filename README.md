# IfcModelAuditor

A multi-engine BIM validation platform — a C# rule engine and a Python
auditor write structured results into a shared SQLite data layer, surfaced
through a unified queryable web interface.

Built to demonstrate end-to-end data systems work: ingestion, persistence,
querying, and an interactive application layer — using IFC (BIM) models as
the dataset.

---

## System Architecture

```
IFC File
    ├── Python Auditor (IfcOpenShell)
    │       ↓
    │   Validation + Element Extraction
    │       ↓
    └── C# IfcQA Engine (xBIM)
            ↓
        Rule-based Validation
            ↓
    ┌───────────────────────┐
    │    SQLite (audit.db)  │  ← shared data contract
    │  audit_runs           │
    │  issues (source col)  │
    │  element_counts       │
    └───────────────────────┘
            ↓
    Query Layer (Python)
            ↓
    Flask API  ──→  JSON over HTTP
            ↓
    Web Application
    - Runs list with stat cards
    - Issues table per run
    - Filter by engine (Python / IfcQA)
    - Filter by IFC class
    - Severity color coding
```

Two consumers read from the same data layer independently:
- **CLI** — for direct querying and pipeline integration
- **Web app** — for interactive multi-engine exploration

---

## Features

**Multi-engine data pipeline**
- Python auditor parses IFC models via IfcOpenShell, extracts structured
  element data, runs validation rules, persists results to SQLite
- C# IfcQA engine runs configurable JSON-driven rulesets via xBIM,
  writes results to the same SQLite database with `--sqlite` flag
- Both engines write to a shared schema — `source` column identifies
  which engine produced each issue

**Query layer**
- Get all audit runs ordered by timestamp
- Get all issues for a specific run, optionally filtered by source engine
- Aggregate issue counts by rule code or IFC class
- All queries return structured `List[dict]` — clean, typed, composable

**Web application**
- Lists all audit runs with summary statistics
- Click into any run to explore its issues
- Filter by engine (Python / IfcQA) using chip toggles
- Filter by IFC class simultaneously
- Severity color coding: Error (red), Warning (amber), Info (blue)
- Consistent design language with the IfcQA HTML report

**CLI**
- Full audit pipeline from a single command
- Query subcommand for direct database inspection
- Designed for scripting and pipeline integration

---

## Project Structure

```
├── auditor/
│   ├── app/
│   │   ├── main.py          CLI entry point (audit + query subcommands)
│   │   └── server.py        Flask API server
│   ├── core/
│   │   ├── model.py         Data models: ElementInfo, IssueRecord, AuditReport
│   │   └── auditor.py       Validation logic
│   ├── infrastructure/
│   │   ├── ifc_reader.py    IFC parsing via IfcOpenShell
│   │   ├── sqlite_writer.py SQLite write + query layer
│   │   ├── json_writer.py
│   │   ├── csv_writer.py
│   │   └── console_writer.py
│   └── web/
│       ├── index.html       Single-page web application
│       ├── style.css
│       └── app.js
├── src/                     IfcQA C# validation engine
│   ├── IfcQa.Core/
│   └── IfcQa.Cli/
│       └── SqliteWriter.cs  Shared SQLite writer
├── output/                  Shared output directory (audit.db)
├── samples/                 Sample IFC files
└── rulesets/                IfcQA JSON rulesets
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| IFC parsing (Python) | IfcOpenShell |
| IFC parsing (C#) | xBIM Toolkit |
| Validation engine | Python + C# / .NET |
| Persistence | SQLite |
| API server | Flask |
| Web application | HTML / CSS / JS (no framework) |

---

## Installation

```bash
# Python dependencies
pip install -r auditor/requirements.txt

# IfcQA — download the Windows release from the releases page
# or build from source with: dotnet build
```

---

## Usage

### Run the Python auditor

```bash
python auditor/app/main.py audit samples/test.ifc --output output
```

### Run IfcQA with SQLite output

```powershell
.\ifcqa.exe check samples\test.ifc -o output --sqlite
```

Both engines write to `output/audit.db`.

### Query the database (CLI)

```bash
# List all audit runs from both engines
python auditor/app/main.py query --runs

# Get all issues for a specific run
python auditor/app/main.py query --issues-by-run 1

# Issue counts by rule code (latest run)
python auditor/app/main.py query --issue-summary

# Issue counts by IFC class (latest run)
python auditor/app/main.py query --issue-by-class
```

### Launch the web application

```bash
python auditor/app/server.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Database Schema

```sql
audit_runs (
    id               INTEGER PRIMARY KEY,
    source_file      TEXT,
    run_timestamp    TEXT,
    total_elements   INTEGER,
    total_issues     INTEGER
)

issues (
    id             INTEGER PRIMARY KEY,
    audit_run_id   INTEGER,   -- foreign key → audit_runs.id
    issue_code     TEXT,      -- RuleId in IfcQA
    severity       TEXT,      -- Error / Warning / Info (IfcQA); NULL (Python for now)
    message        TEXT,
    global_id      TEXT,
    ifc_class      TEXT,
    element_name   TEXT,
    path           TEXT,      -- IfcQA trace metadata
    expected       TEXT,      -- IfcQA trace metadata
    actual         TEXT,      -- IfcQA trace metadata
    source         TEXT       -- 'python' or 'ifcqa'
)

element_counts (
    id             INTEGER PRIMARY KEY,
    audit_run_id   INTEGER,   -- foreign key → audit_runs.id
    ifc_class      TEXT,
    element_count  INTEGER
)
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/runs` | All audit runs, newest first |
| GET | `/runs/<id>/issues` | All issues for a run |
| GET | `/runs/<id>/issues?source=python` | Python auditor issues only |
| GET | `/runs/<id>/issues?source=ifcqa` | IfcQA issues only |
| GET | `/runs/<id>/summary` | Issue counts by rule code |
| GET | `/runs/<id>/issues/by-class` | Issue counts by IFC class |

---

## Related Project

**[IfcQA](https://github.com/tommylee0923/ifcqa-tool)** — the C# / .NET
rule-based validation engine that feeds into this system via the shared
SQLite data contract.

---

## Status

Active development.

- Milestone 1 — SQLite data layer + CLI query commands
- Milestone 2 — Flask API
- Milestone 3 — Web application
- Milestone 4 — Polish + documentation
- Milestone 5 — IfcQA integration (multi-engine platform)