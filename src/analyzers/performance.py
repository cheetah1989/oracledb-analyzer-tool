"""
Performance Analyzer

Analyzes SQL workload, active sessions and wait events.
"""

class PerformanceAnalyzer:

    def __init__(self, data, rules):
        self.data = data
        self.rules = rules
        self.findings = []

    def add_finding(
        self,
        severity,
        finding,
        evidence,
        recommendation
    ):
        self.findings.append({
            "severity": severity,
            "category": "performance",
            "finding": finding,
            "evidence": evidence,
            "recommendation": recommendation
        })

    def analyze_cpu(self):

        rows = (
            self.data
            .get("performance", {})
            .get("top_cpu", [])
        )

        rules = self.rules.get("sql", {})

        critical = rules.get(
            "cpu_seconds", {}
        ).get("critical", 300)

        warning = rules.get(
            "cpu_seconds", {}
        ).get("warning", 100)

        for row in rows:

            cpu = row.get("cpu_time")

            if cpu is None:
                continue

            try:
                cpu = float(cpu)
            except (ValueError, TypeError):
                continue

            sql_id = row.get(
                "sql_id",
                "UNKNOWN"
            )

            evidence = {
                "sql_id": sql_id,
                "cpu_time": cpu,
                "executions": row.get("executions"),
                "module": row.get("module"),
                "sql_text": row.get("sql_text")
            }

            if cpu >= critical:

                self.add_finding(
                    "CRITICAL",
                    (
                        f"SQL {sql_id} has very high "
                        f"CPU consumption."
                    ),
                    evidence,
                    (
                        "Review the execution plan, "
                        "logical I/O, predicates, joins "
                        "and indexing strategy."
                    )
                )

            elif cpu >= warning:

                self.add_finding(
                    "WARNING",
                    (
                        f"SQL {sql_id} has elevated "
                        f"CPU consumption."
                    ),
                    evidence,
                    (
                        "Review execution statistics and "
                        "execution plan for optimization opportunities."
                    )
                )

    def analyze_elapsed(self):

        rows = (
            self.data
            .get("performance", {})
            .get("top_elapsed", [])
        )

        rules = self.rules.get("sql", {})

        critical = rules.get(
            "elapsed_seconds", {}
        ).get("critical", 600)

        warning = rules.get(
            "elapsed_seconds", {}
        ).get("warning", 300)

        for row in rows:

            elapsed = row.get("elapsed_time")

            if elapsed is None:
                continue

            try:
                elapsed = float(elapsed)
            except (ValueError, TypeError):
                continue

            sql_id = row.get(
                "sql_id",
                "UNKNOWN"
            )

            evidence = {
                "sql_id": sql_id,
                "elapsed_time": elapsed,
                "executions": row.get("executions"),
                "module": row.get("module"),
                "sql_text": row.get("sql_text")
            }

            if elapsed >= critical:

                self.add_finding(
                    "CRITICAL",
                    (
                        f"SQL {sql_id} has very high "
                        f"elapsed time."
                    ),
                    evidence,
                    (
                        "Review execution plan and wait "
                        "events to determine whether the "
                        "time is CPU, I/O or concurrency related."
                    )
                )

            elif elapsed >= warning:

                self.add_finding(
                    "WARNING",
                    (
                        f"SQL {sql_id} has elevated "
                        f"elapsed time."
                    ),
                    evidence,
                    (
                        "Review execution statistics, "
                        "wait events and execution plan."
                    )
                )

    def analyze_active_sessions(self):

        rows = (
            self.data
            .get("performance", {})
            .get("active_sessions", [])
        )

        # Events that are normally idle/background waits
        # and should not become performance findings.
        idle_wait_classes = {
            "Idle"
        }

        # Group sessions by SQL_ID so that multiple sessions
        # running the same SQL don't generate duplicate findings.
        sql_sessions = {}

        for row in rows:

            sql_id = row.get(
                "sql_id",
                "UNKNOWN"
            )

            wait_class = row.get(
                "wait_class"
            )

            if wait_class in idle_wait_classes:
                continue

            if sql_id not in sql_sessions:
                sql_sessions[sql_id] = []

            sql_sessions[sql_id].append(row)

        for sql_id, sessions in sql_sessions.items():
            events = sorted(
                {
                    session.get("event")
                    for session in sessions
                    if session.get("event")
                }
            )

            wait_classes = sorted(
                {
                    session.get("wait_class")
                    for session in sessions
                    if session.get("wait_class")
                }
            )

            modules = sorted(
                {
                    session.get("module")
                    for session in sessions
                    if session.get("module")
                }
            )

            evidence = {
                "sql_id": sql_id,
                "active_session_count": len(sessions),
                "events": events,
                "wait_classes": wait_classes,
                "modules": modules
            }

            self.add_finding(
                "INFO",
                (
                    f"SQL {sql_id} has "
                    f"{len(sessions)} active session(s) "
                    f"with non-idle wait activity."
                ),
                evidence,
                (
                    "Correlate this SQL with CPU, elapsed time, "
                    "I/O and wait-event metrics before determining "
                    "whether optimization is required."
                )
            )

    def correlate_sql(self):
        """
        Combine SQL metrics from the different performance
        collections using SQL_ID as the correlation key.
        """

        performance = self.data.get(
            "performance",
            {}
        )

        sql_metrics = {}

        sources = [
            "top_cpu",
            "top_elapsed",
            "top_io",
            "top_buffer_gets",
            "top_executions"
        ]

        for source in sources:

            rows = performance.get(
                source,
                []
            )

            for row in rows:

                sql_id = row.get("sql_id")

                if not sql_id:
                    continue

                if sql_id not in sql_metrics:
                    sql_metrics[sql_id] = {
                        "sql_id": sql_id,
                        "plan_hash_value": row.get(
                            "plan_hash_value"
                        ),
                        "parsing_schema_name": row.get(
                            "parsing_schema_name"
                        ),
                        "module": row.get(
                            "module"
                        ),
                        "action": row.get(
                            "action"
                        ),
                        "sql_text": row.get(
                            "sql_text"
                        )
                    }

                sql_metrics[sql_id][source] = row

        return sql_metrics

    def analyze_sql_correlation(self):

        sql_metrics = self.correlate_sql()

        for sql_id, metrics in sql_metrics.items():

            dimensions = []

            classifications = self.classify_sql(
                metrics
            )

            for dimension in [
                "top_cpu",
                "top_elapsed",
                "top_io",
                "top_buffer_gets",
                "top_executions"
            ]:

                   if dimension in metrics:
                     dimensions.append(dimension)

            # Only report SQL that appears in at least
            # two independent performance dimensions.
            if len(dimensions) < 2:
                continue

            cpu = metrics.get(
                "top_cpu",
                {}
            )

            elapsed = metrics.get(
                "top_elapsed",
                {}
            )

            io = metrics.get(
                "top_io",
                {}
            )

            buffer_gets = metrics.get(
                "top_buffer_gets",
                {}
            )

            executions = metrics.get(
                "top_executions",
                {}
            )

            evidence = {
                "workload_type": self.classify_workload(metrics),
                "sql_id": sql_id,
                "module": metrics.get("module"),
                "action": metrics.get("action"),
                "parsing_schema_name": metrics.get(
                    "parsing_schema_name"
                ),
                "dimensions": dimensions,

                "cpu_seconds": cpu.get(
                    "cpu_seconds"
                ),

                "elapsed_seconds": elapsed.get(
                    "elapsed_seconds"
                ),

                "disk_reads": io.get(
                    "disk_reads"
                ),

                "direct_reads": io.get(
                    "direct_reads"
                ),

                "direct_writes": io.get(
                    "direct_writes"
                ),

                "buffer_gets": buffer_gets.get(
                    "buffer_gets"
                ),

                "executions": executions.get(
                    "executions"
                ),

                "sql_text": metrics.get(
                    "sql_text"
                ),
                "classifications": classifications
            }


            if classifications:
                self.add_finding(
                    "WARNING",
                    (
                        f"SQL {sql_id} classified as "
                        f"{', '.join(classifications)}."
                    ),
                    evidence,
                    (
                        "Review the correlated workload metrics, "
                        "execution plan and application context "
                        "before taking optimization action."
                    )
                )

            else:
                self.add_finding(
                    "INFO",
                    (
                        f"SQL {sql_id} appears in "
                        f"{len(dimensions)} performance dimensions "
                        f"({', '.join(dimensions)})."
                    ),
                    evidence,
                    (
                        "Review the correlated workload metrics "
                        "and execution plan to determine whether "
                        "this SQL represents a significant "
                        "performance or resource-consumption concern."
                    )
                )

            # self.add_finding(
            #     "INFO",
            #
            #     (
            #         f"SQL {sql_id} appears in "
            #         f"{len(dimensions)} performance dimensions "
            #         f"({', '.join(dimensions)})."
            #     ),
            #
            #     evidence,
            #
            #     (
            #         "Review the correlated workload metrics "
            #         "and execution plan to determine whether "
            #         "this SQL represents a significant "
            #         "performance or resource-consumption concern."
            #     )
            # )
            #
            # self.add_finding(
            #     "WARNING",
            #     (
            #       f"SQL {sql_id} classified as "
            #       f"{', '.join(classifications)}."
            #     ),
            #     evidence,
            #     (
            #         "Review the correlated workload metrics, "
            #         "execution plan and application context "
            #         "before taking optimization action."
            #     )
            # )

    def classify_sql(self, metrics):
        """
        Classify SQL based on correlated workload characteristics.
        """

        cpu = metrics.get("top_cpu", {})
        elapsed = metrics.get("top_elapsed", {})
        io = metrics.get("top_io", {})
        buffer_gets = metrics.get("top_buffer_gets", {})
        executions = metrics.get("top_executions", {})

        cpu_seconds = float(
            cpu.get("cpu_seconds") or 0
        )

        elapsed_seconds = float(
            elapsed.get("elapsed_seconds") or 0
        )

        disk_reads = int(
            io.get("disk_reads") or 0
        )

        buffer_get_count = int(
            buffer_gets.get("buffer_gets") or 0
        )

        execution_count = int(
            executions.get("executions") or
            cpu.get("executions") or
            elapsed.get("executions") or
            0
        )

        classifications = []

        # ---------------------------------------------------------
        # CPU intensive
        # ---------------------------------------------------------

        if cpu_seconds >= 10000:
            classifications.append(
                "CPU_INTENSIVE"
            )

        # ---------------------------------------------------------
        # High elapsed time
        # ---------------------------------------------------------

        if elapsed_seconds >= 10000:
            classifications.append(
                "HIGH_ELAPSED_TIME"
            )

        # ---------------------------------------------------------
        # Heavy physical I/O
        # ---------------------------------------------------------

        if disk_reads >= 100000000:
            classifications.append(
                "IO_INTENSIVE"
            )

        # ---------------------------------------------------------
        # Heavy logical I/O
        # ---------------------------------------------------------

        if buffer_get_count >= 1000000000:
            classifications.append(
                "BUFFER_GET_INTENSIVE"
            )

        # ---------------------------------------------------------
        # Very high execution frequency
        # ---------------------------------------------------------

        if execution_count >= 1000000:
            classifications.append(
                "HIGH_EXECUTION_FREQUENCY"
            )

        return classifications

    def classify_workload(self, metrics):
        """
        Identify whether SQL appears to be application,
        Oracle internal, scheduler or unknown workload.
        """

        schema = (
                metrics.get("parsing_schema_name")
                or ""
        ).upper()

        module = (
                metrics.get("module")
                or ""
        ).upper()

        if module == "DBMS_SCHEDULER":
            return "ORACLE_SCHEDULER"

        if schema in {
            "SYS",
            "SYSTEM",
            "SYSMAN",
            "DBSNMP"
        }:
            return "ORACLE_INTERNAL"

        if schema == "APPS":
            return "APPLICATION"

        return "OTHER"

    def analyze(self):

        self.findings = []

        self.analyze_cpu()
        self.analyze_elapsed()
        self.analyze_active_sessions()
        self.analyze_sql_correlation()

        return self.findings