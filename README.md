# IfcModelAuditor

A data pipeline that ingests BIM models, runs validation, stores structured results in SQLite, and surfaces them through a queryable web interface.

Built to demonstrate end-to-end data systems work: ingestion, persistence, querying, and an interactive application layer — using IFC (BIM) models as the dataset.

---

## System Architecture

```
IFC File
    ↓
Python Ingestion Layer       reads model, extracts structured elements
    ↓
Validation Engine            runs rule-based checks, generates issues
    ↓
SQLite                       central persistence — audit_runs, issues, element_counts
    ↓
Query Layer (Python)         typed query functions over the SQLite layer
    ↓
Flask API                    exposes query results as JSON over HTTP
    ↓
Web Application              browser-based interface for exploring runs and issues
```

Two consumers read from the same data layer independently:
- **CLI** — for direct querying and pipeline integration
- **Web app** — for interactive exploration

---

## Features

**Data pipeline**
- Parses IFC model files using IfcOpenShell
- Extracts structured element data (`global_id`, `ifc_class`, `name`)
- Runs configurable validation rules and generates typed issue records
- Persists all results to SQLite with full multi-run history

**Query layer**
- Get all audit runs ordered by timestamp
- Get all issues for a specific run
- Aggregate issue counts by rule code or IFC class
- All queries return structured `List[dict]` — clean, typed, composable

**Web application**
- Lists all audit runs with summary statistics
- Click into any run to explore its issues
- Filter issues dynamically by IFC class using chip toggles
- Consistent design language with the companion IfcQA tool

**CLI**
- Full audit pipeline from a single command
- Query subcommand for direct database inspection
- Designed for scripting and pipeline integration

---

## Project Structure

```
├── app/
│   ├── main.py          # CLI entry point (audit + query subcommands)
│   └── server.py        # Flask API server
├── core/
│   ├── model.py         # Data models: ElementInfo, IssueRecord, AuditReport
│   └── auditor.py       # Validation logic
├── infrastructure/
│   ├── ifc_reader.py    # IFC parsing via IfcOpenShell
│   ├── sqlite_writer.py # SQLite write + query layer
│   ├── json_writer.py
│   ├── csv_writer.py
│   └── console_writer.py
├── web/
│   ├── index.html       # Single-page web application
│   ├── style.css
│   └── app.js
├── output/              # Generated audit.db and report files
└── samples/             # Sample IFC files
```

---

## Tech Stack

- **Python** — ingestion, validation, query layer, API
- **SQLite** — persistent relational storage
- **Flask** — lightweight HTTP API server
- **IfcOpenShell** — IFC model parsing
- **HTML / CSS / JS** — web application

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

### Run an audit

```bash
python app/main.py audit samples/test.ifc
```

Optional flags:
```bash
--output <dir>   Output directory (default: output)
--no-console     Disable console output
--no-json        Disable JSON output
--no-csv         Disable CSV output
--no-sqlite      Disable SQLite output
```

### Query the database (CLI)

```bash
# List all audit runs
python app/main.py query --runs

# Get all issues for a specific run
python app/main.py query --issues-by-run 1

# Issue counts by rule code (latest run)
python app/main.py query --issue-summary

# Issue counts by IFC class (latest run)
python app/main.py query --issue-by-class
```

### Launch the web application

```bash
python app/server.py
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
    issue_code     TEXT,
    message        TEXT,
    global_id      TEXT,
    ifc_class      TEXT,
    element_name   TEXT
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

| Method | Endpoint                        | Description                        |
|--------|---------------------------------|------------------------------------|
| GET    | `/runs`                         | All audit runs, newest first       |
| GET    | `/runs/<id>/issues`             | All issues for a specific run      |
| GET    | `/runs/<id>/summary`            | Issue counts by rule code          |
| GET    | `/runs/<id>/issues/by-class`    | Issue counts by IFC class          |

---

## Related Project

**[IfcQA](https://github.com/tommylee0923/ifc-quality-gate)** — a C# / .NET
rule-based validation engine for IFC models. Planned integration: IfcQA will
write results into the same SQLite schema, making this a multi-engine audit
platform with a shared data layer and unified web interface.

---

## Status

Active development. Current focus: completing the web application layer and
preparing for IfcQA integration.