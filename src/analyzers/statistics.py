class StatisticsAnalyzer:

    def __init__(self, data):
        self.data = data
        self.findings = []

    def add_finding(
        self,
        severity,
        message,
        evidence,
        recommendation
    ):
        self.findings.append({
            "severity": severity,
            "message": message,
            "evidence": evidence,
            "recommendation": recommendation
        })

    def analyze_stale_statistics(self):

        rows = (
            self.data
            .get("statistics", {})
            .get("stale_stats", [])
        )

        for row in rows:

            owner = row.get("owner")
            table_name = row.get("table_name")
            partition_name = row.get("partition_name")
            num_rows = row.get("num_rows")
            blocks = row.get("blocks")
            last_analyzed = row.get("last_analyzed")
            stale_stats = row.get("stale_stats")

            evidence = {
                "owner": owner,
                "table_name": table_name,
                "partition_name": partition_name,
                "num_rows": num_rows,
                "blocks": blocks,
                "last_analyzed": last_analyzed,
                "stale_stats": stale_stats
            }

            object_name = f"{owner}.{table_name}"

            if partition_name:
                object_name = (
                    f"{object_name} "
                    f"(partition: {partition_name})"
                )

            self.add_finding(
                "WARNING",
                (
                    f"Optimizer statistics for "
                    f"{object_name} are marked as stale."
                ),
                evidence,
                (
                    "Review table modification activity and "
                    "statistics freshness. Determine whether "
                    "stale statistics could affect optimizer "
                    "cardinality estimates or execution plans. "
                    "Gather statistics when appropriate."
                )
            )

    def analyze_stale_accessed_tables(self):

        statistics = self.data.get(
            "statistics",
            {}
        )

        stale_rows = statistics.get(
            "stale_stats",
            []
        )

        access_rows = statistics.get(
            "table_access",
            []
        )

        accessed_tables = {}

        for row in access_rows:

            owner = row.get("owner")
            table_name = row.get("table_name")

            if not owner or not table_name:
                continue

            key = (
                owner.upper(),
                table_name.upper()
            )

            accessed_tables[key] = row

        for row in stale_rows:

            owner = row.get("owner")
            table_name = row.get("table_name")

            if not owner or not table_name:
                continue

            key = (
                owner.upper(),
                table_name.upper()
            )

            access = accessed_tables.get(key)

            if not access:
                continue

            sql_count = access.get(
                "sql_count",
                0
            ) or 0

            plan_operations = access.get(
                "plan_operations",
                0
            ) or 0

            if sql_count >= 20:

                severity = "WARNING"

                message = (
                    f"Table {owner}.{table_name} has "
                    f"stale optimizer statistics and is "
                    f"referenced by {sql_count} SQL statements."
                )

            else:

                severity = "INFO"

                message = (
                    f"Table {owner}.{table_name} has "
                    f"stale optimizer statistics and "
                    f"recent SQL activity."
                )

            evidence = {
                "owner": owner,
                "table_name": table_name,
                "last_analyzed": row.get(
                    "last_analyzed"
                ),
                "stale_stats": row.get(
                    "stale_stats"
                ),
                "num_rows": row.get(
                    "num_rows"
                ),
                "plan_operations": plan_operations,
                "sql_count": sql_count,
                "last_seen": access.get(
                    "last_seen"
                )
            }

            self.add_finding(
                severity,
                message,
                evidence,
                (
                    "Review statistics freshness and "
                    "table workload. Prioritize statistics "
                    "gathering where stale statistics may "
                    "affect optimizer cardinality estimates "
                    "or execution plan selection."
                )
            )

    def analyze_histograms(self):

        rows = (
            self.data
            .get("statistics", {})
            .get("histograms", [])
        )

        for row in rows:
            owner = row.get("owner")
            table_name = row.get("table_name")
            column_name = row.get("column_name")

            evidence = {
                "owner": owner,
                "table_name": table_name,
                "column_name": column_name,
                "num_distinct": row.get("num_distinct"),
                "num_nulls": row.get("num_nulls"),
                "num_buckets": row.get("num_buckets"),
                "histogram": row.get("histogram"),
                "density": row.get("density"),
                "last_analyzed": row.get("last_analyzed")
            }

            self.add_finding(
                "INFO",
                (
                    f"Histogram detected on "
                    f"{owner}.{table_name}.{column_name}."
                ),
                evidence,
                (
                    "Review histogram usage when investigating "
                    "cardinality estimates or execution plan "
                    "changes for SQL referencing this column."
                )
            )

    def analyze_column_skew(self):

        statistics = self.data.get(
            "statistics",
            {}
        )

        skew_rows = statistics.get(
            "column_skew",
            []
        )

        access_rows = statistics.get(
            "table_access",
            []
        )

        accessed_tables = {}

        for row in access_rows:

            owner = row.get("owner")
            table_name = row.get("table_name")

            if not owner or not table_name:
                continue

            key = (
                owner.upper(),
                table_name.upper()
            )

            accessed_tables[key] = row

        for row in skew_rows:

            owner = row.get("owner")
            table_name = row.get("table_name")
            column_name = row.get("column_name")

            if not owner or not table_name:
                continue

            key = (
                owner.upper(),
                table_name.upper()
            )

            access = accessed_tables.get(key)

            if not access:
                continue

            sql_count = access.get(
                "sql_count",
                0
            ) or 0

            plan_operations = access.get(
                "plan_operations",
                0
            ) or 0

            evidence = {
                "owner": owner,
                "table_name": table_name,
                "column_name": column_name,
                "num_distinct": row.get("num_distinct"),
                "num_nulls": row.get("num_nulls"),
                "num_buckets": row.get("num_buckets"),
                "histogram": row.get("histogram"),
                "density": row.get("density"),
                "sample_size": row.get("sample_size"),
                "last_analyzed": row.get("last_analyzed"),
                "sql_count": sql_count,
                "plan_operations": plan_operations,
                "last_seen": access.get("last_seen")
            }

            self.add_finding(
                "INFO",
                (
                     f"Column {owner}.{table_name}.{column_name} "
                     f"has a skewed data distribution and is referenced "
                     f"by {sql_count} SQL statements."
                ),
                evidence,
                (
                    "Review this column when investigating "
                    "cardinality estimation, selectivity or "
                    "execution plan issues. Existing histogram "
                    "information should be considered when "
                    "evaluating optimizer behavior."
                )
            )

    def analyze(self):

        self.findings = []

        self.analyze_stale_statistics()
        self.analyze_stale_accessed_tables()
        #self.analyze_histograms()
        self.analyze_column_skew()

        return self.findings