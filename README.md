Oracle Environment Analyzer

A Python-based Oracle Database diagnostic tool that collects database environment information, analyzes configuration, storage, performance, optimizer statistics, indexes and stability indicators, and produces structured, evidence-based findings.

The project is designed as a read-only DBA diagnostic and assessment tool.
What does it do?

The analyzer connects to an Oracle Database and collects information across multiple operational areas:

Environment
Storage
Configuration
Server
Performance
Statistics
Indexes
Stability

The collected information is stored as structured JSON and passed through independent analyzers.

Oracle Database
      |
      v
Data Collector
      |
      v
Structured JSON
      |
      v
+-------------------------+
| Analysis Engine         |
|                         |
| Storage                 |
| Configuration           |
| Performance             |
| Statistics              |
| Indexes                 |
| Stability               |
+-------------------------+
      |
      v
Findings
      |
      v
Severity + Evidence + Recommendation
Key Features
Environment

Collects:

Database information
Instance information
OS statistics
Important Oracle parameters
Storage

Analyzes:

Database size
Tablespace utilization
Datafiles
TEMP
UNDO
ASM diskgroups

Example:

[CRITICAL] Tablespace APPS_TS_TX_DATA is critically utilized at 99.74%.
Configuration

Analyzes:

Oracle memory configuration
PROCESSES
SESSIONS
Optimizer parameters
Cursor configuration
Parallelism
Performance

Collects and correlates:

Top CPU SQL
Top elapsed-time SQL
Top I/O SQL
Top buffer-get SQL
Highly executed SQL
Active sessions
Wait events

The analyzer can classify SQL workloads such as:

CPU_INTENSIVE
HIGH_ELAPSED_TIME
IO_INTENSIVE
BUFFER_GET_INTENSIVE
HIGH_EXECUTION_FREQUENCY

A SQL statement can receive multiple classifications based on correlated workload dimensions.

Example:

[WARNING] SQL 8szmwam7fysa3 classified as
CPU_INTENSIVE, HIGH_ELAPSED_TIME,
IO_INTENSIVE, HIGH_EXECUTION_FREQUENCY.
Statistics

Analyzes:

Table statistics
Index statistics
Stale statistics
Histograms
Table access patterns
Column skew

The analyzer can correlate column statistics with table access activity.

Example:

[INFO] Column APPLSYS.FND_CURRENCIES.DERIVE_TYPE
has a skewed data distribution and is referenced
by 10 SQL statements.
Indexes

Currently checks:

Unused indexes
Duplicate indexes

Index findings are treated as investigation candidates rather than automatic recommendations to drop indexes.

Stability

Analyzes:

Blocking sessions
Long transactions
Invalid objects
Redo configuration/activity
Archive log information
Recovery area
Database status

Example:

[WARNING] 1 long transactions record(s) detected.
Output Format

Every finding follows a consistent structure:

{
    "severity": "WARNING",
    "finding": "Optimizer statistics for APPLSYS.X are marked as stale.",
    "evidence": {
        "owner": "APPLSYS",
        "table_name": "X",
        "stale_stats": "YES"
    },
    "recommendation": "Review table modification activity..."
}

This makes the output suitable for future integration with:

APIs
Dashboards
Monitoring systems
Incident management
AI/LLM applications
Example
Performance Analysis
======================


[WARNING] SQL 6mcpb06rctk0x classified as
CPU_INTENSIVE, HIGH_ELAPSED_TIME, IO_INTENSIVE.


Evidence:
{
    'sql_id': '6mcpb06rctk0x',
    'workload_type': 'ORACLE_SCHEDULER',
    'cpu_seconds': 414488.79,
    'elapsed_seconds': 633183.62,
    'disk_reads': 2142347017,
    ...
}


Recommendation:
Review the correlated workload metrics, execution plan
and application context before taking optimization action.
Project Structure

The project follows a modular design:

oracle-environment-analyzer/
|
├── src/
│   ├── collectors/
│   ├── analyzers/
│   ├── rules/
│   ├── sql/
│   └── main.py
|
├── tests/
│   ├── test-configuration-analyzer.py
│   ├── test-storage-analyzer.py
│   ├── test-performance-analyzer.py
│   ├── test-statistics-analyzer.py
│   ├── test-index-analyzer.py
│   ├── test-stability-analyzer.py
│   └── test-json-struct.py
|
├── output/
│   └── <database>/
│       └── environment_<timestamp>.json
|
├── requirements.txt
└── README.md

The exact directory structure may evolve as additional components are introduced.

Running the Analyzer

Activate the Python virtual environment and run:

python -m src.main

The analyzer connects to the configured Oracle database and performs the collection process.

Example:

Collecting category: environment
--------------------------------
  Collecting: database
  Collecting: instance
  Collecting: os_stat
  Collecting: parameters


Collecting category: storage
--------------------------------
  Collecting: database_size
  Collecting: tablespace_usage
  Collecting: datafiles
  Collecting: temp_usage
  Collecting: undo_usage

The collected environment is saved as JSON.

Running Individual Analyzers

Each analyzer can be tested independently.

python -m tests.test-storage-analyzer
python -m tests.test-configuration-analyzer
python -m tests.test-performance-analyzer
python -m tests.test-statistics-analyzer
python -m tests.test-index-analyzer
python -m tests.test-stability-analyzer

This makes it easier to develop and validate individual analysis components without running the entire collection process every time.

Design Philosophy

The project follows five principles:

1. Read-only

The analyzer should inspect the database rather than modify it.

2. Evidence first

Every meaningful finding should be supported by collected database information.

3. Correlation over isolated metrics

A SQL appearing across CPU, elapsed time and I/O dimensions is more significant than a SQL appearing in only one list.

4. Conservative recommendations

The analyzer identifies areas requiring DBA investigation. It does not blindly execute remediation.

5. Modular architecture

Collectors and analyzers are separated so new capabilities can be added independently.

Current Scope

The current POC supports:

✓ Oracle environment discovery
✓ Storage analysis
✓ Tablespace utilization
✓ TEMP / UNDO analysis
✓ Memory configuration analysis
✓ Process/session configuration
✓ Optimizer configuration
✓ Cursor configuration
✓ Parallelism configuration
✓ CPU SQL analysis
✓ Elapsed SQL analysis
✓ I/O SQL analysis
✓ Buffer-get analysis
✓ Execution-frequency analysis
✓ Active-session analysis
✓ Wait-event analysis
✓ Stale statistics analysis
✓ Histogram analysis
✓ Column-skew analysis
✓ Table-access correlation
✓ Unused-index detection
✓ Duplicate-index detection
✓ Blocking-session detection
✓ Long-transaction detection
✓ Invalid-object detection
✓ Redo analysis
✓ Structured JSON output
✓ Rule-based findings
Limitations

This is currently a POC and should not be considered an automated Oracle tuning platform.

Current limitations include:

Historical trending is not implemented.
Thresholds require environment-specific tuning.
Performance analysis depends on the available Oracle workload data.
Index usage requires an appropriate observation period.
Some statistics queries can be expensive on large environments.
ASM information depends on the database/storage configuration.
The analyzer does not automatically modify database configuration.
Detailed execution-plan analysis is not yet part of the analyzer.
Findings should be reviewed by a DBA before remediation.
Future Direction

The long-term goal is to use this analyzer as the diagnostic foundation for an AI-assisted DBA platform.

Potential architecture:

                   Oracle Database
                          |
                          v
                  Environment Analyzer
                          |
                          v
                    Structured JSON
                          |
                          v
                   Rule / Correlation
                        Engine
                          |
                          v
                       Findings
                          |
                          v
                    DBA AI Agent
                          |
              +-----------+-----------+
              |                       |
        Explanation              Investigation
              |                       |
              +-----------+-----------+
                          |
                          v
                    DBA Decision

The important architectural boundary is that the AI layer should consume validated database evidence rather than inventing database state.

Why this project?

Oracle DBAs already have the SQL knowledge required to investigate most database problems.

The challenge is turning that knowledge into a repeatable process that can:

Collect the right information.
Structure it consistently.
Correlate related signals.
Prioritize findings.
Provide evidence.
Give the DBA a sensible starting point for investigation.

That is what this project is intended to solve.