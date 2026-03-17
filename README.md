# IFC Model Auditor (Python)

Lightweight Python CLI tool for inspecting IFC models and generating structured audit outputs.

This project is part of an ongoing effort to build practical BIM data tools and strengthen AEC software development skills through real implementations.

---

## Overview

IFC Model Auditor reads an IFC file, extracts element data, and produces a structured audit of the model.

The tool focuses on:

- understanding model composition
- identifying basic data quality issues
- exporting results in multiple formats for different use cases

---

## Features

- Extracts all `IfcProduct` elements from an IFC model  
- Counts elements by IFC class  
- Detects missing element names (data quality check)  
- Generates multiple output formats:
  - Console (human-readable)
  - JSON (structured data)
  - CSV (spreadsheet-friendly)
  - SQLite (queryable dataset)

---

## Example Outputs

### Console Output
- Summary of total elements and issues  
- Element counts by class  
- Detailed issue listing  

### JSON
- Full structured audit report including metadata and issues  

### CSV
- Element counts by IFC class  
- (Optional) issue records  

### SQLite
- Persistent relational dataset for querying and analysis  

Tables:
- `audit_runs`
- `element_counts`
- `issues`

---

## Project Structure

```
├── app
│   └── main.py              # CLI entry point
├── core
│   ├── model.py            # Data models (ElementInfo, IssueRecord, AuditReport)
│   └── auditor.py          # Core audit logic
├── infrastructure
│   ├── ifc_reader.py       # IFC parsing (IfcOpenShell)
│   ├── console_writer.py
│   ├── json_writer.py
│   ├── csv_writer.py
│   └── sqlite_writer.py    # SQLite persistence layer
├── output                  # Generated reports
├── samples                 # Sample IFC files
```

---

## Architecture

The project follows a simple layered structure:

- **Core** → business logic and data models  
- **Infrastructure** → external I/O (IFC, file writing, database)  
- **App** → CLI interface and orchestration  

This separation keeps the audit logic independent from output formats and data sources.

---

## How It Works

1. Load IFC file using IfcOpenShell  
2. Extract element data (`global_id`, `ifc_class`, `name`)  
3. Run audit:
   - count elements by class
   - detect missing names  
4. Generate structured `AuditReport`  
5. Export results to selected outputs  

---

## Installation

```bash
pip install -r requirement.txt
```

---

## Usage

Basic run:

```bash
python app/main.py samples/test.ifc
```

Optional flags:

```bash
--output <dir>        # Output directory (default: output)
--no-console         # Disable console output
--no-json            # Disable JSON output
--no-csv             # Disable CSV output
--no-sqlite          # Disable SQLite output
```

Example:

```bash
python app/main.py samples/test.ifc --output output
```

---

## Example Queries (SQLite)

Once `audit.db` is generated:

```sql
SELECT ifc_class, element_count
FROM element_counts
ORDER BY element_count DESC;
```

```sql
SELECT issue_code, COUNT(*) as total
FROM issues
GROUP BY issue_code;
```

---

## Current Scope (v0.1.5)

- CLI-based IFC inspection tool  
- basic validation rule (missing name)  
- multi-format outputs  
- SQLite persistence  

No GUI, API, or external integrations by design.
Under active development.