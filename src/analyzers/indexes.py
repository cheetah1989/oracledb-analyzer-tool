class IndexAnalyzer:

    def __init__(self, data, rules=None):
        self.data = data
        self.rules = rules or {}
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
            "finding": finding,
            "evidence": evidence,
            "recommendation": recommendation
        })

    def analyze_unused_indexes(self):

        indexes = (
            self.data
            .get("indexes", {})
            .get("unused_indexes", [])
        )

        for row in indexes:

            owner = row.get("owner")
            index_name = row.get("index_name")
            table_name = row.get("table_name")

            evidence = row.copy()

            self.add_finding(
                "INFO",
                (
                    f"Index {owner}.{index_name} "
                    f"on table {table_name} "
                    f"is marked as unused."
                ),
                evidence,
                (
                    "Validate index usage across representative "
                    "workloads, application activity and monitoring "
                    "history before considering removal."
                )
            )

    def analyze_duplicate_indexes(self):

        indexes = (
            self.data
            .get("indexes", {})
            .get("duplicate_indexes", [])
        )

        for row in indexes:

            owner = row.get("owner")
            index_name = row.get("index_name")
            table_name = row.get("table_name")

            evidence = row.copy()

            self.add_finding(
                "WARNING",
                (
                    f"Potential duplicate index "
                    f"{owner}.{index_name} detected on "
                    f"table {table_name}."
                ),
                evidence,
                (
                    "Validate column order, uniqueness, constraints, "
                    "foreign keys and workload usage before removing "
                    "or consolidating the index."
                )
            )

    def analyze(self):

        self.findings = []

        self.analyze_unused_indexes()
        self.analyze_duplicate_indexes()

        return self.findings