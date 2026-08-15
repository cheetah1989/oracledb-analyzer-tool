class StabilityAnalyzer:

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

    def analyze_blocking_sessions(self):

        rows = (
            self.data
            .get("stability", {})
            .get("blocking_sessions", [])
        )

        if not rows:
            return

        self.add_finding(
            "WARNING",
            (
                f"{len(rows)} blocking session record(s) "
                f"detected."
            ),
            {
                "blocking_sessions": rows
            },
            (
                "Identify the blocking session, determine the "
                "affected sessions and assess transaction age "
                "before taking corrective action."
            )
        )

    def analyze_long_transactions(self):

        rows = (
                self.data
                .get("stability", {})
                .get("long_transactions", [])
            )

        if not rows:
            return

        self.add_finding(
            "WARNING",
            (
                f"{len(rows)} long transactions record(s) "
                f"detected."
            ),
            {
                "long_transactions": rows
            },
            (
                "Review the transaction age, session details and "
                "application context to determine whether the transaction "
                "is expected or requires corrective action."
            )
        )

    def analyze_invalid_objects(self):

        rows = (
                self.data
                .get("stability", {})
                .get("invalid_objects", [])
            )

        if not rows:
            return

        self.add_finding(
            "WARNING",
            (
                f"{len(rows)} invalid objects "
                f"detected."
            ),
            {
                "invalid_objects": rows
            },
            (
                "Review the invalid objects and their "
                "application context to determine whether the object invalidation "
                "is expected or requires corrective action."
            )
        )

    def analyze_recovery_area(self):

        rows = (
            self.data
            .get("stability", {})
            .get("recovery_area", [])
        )

        if not rows:
            return

        for row in rows:

            used_percent = row.get("used_percent")

            if used_percent is None:
                continue

            if used_percent >= 95:

                severity = "CRITICAL"

                finding = (
                    f"Recovery area is critically utilized "
                    f"at {used_percent:.2f}%."
                )

                recommendation = (
                    "Review recovery area usage immediately. "
                    "Check archived redo logs, backups and other "
                    "recovery files and increase capacity or clean "
                    "up eligible files according to the recovery "
                    "strategy."
                )

            elif used_percent >= 85:

                severity = "WARNING"

                finding = (
                    f"Recovery area has elevated utilization "
                    f"at {used_percent:.2f}%."
                )

                recommendation = (
                    "Monitor recovery area growth and review "
                    "archived logs, backups and recovery files "
                    "before capacity becomes constrained."
                )

            else:
                continue

            self.add_finding(
                severity,
                finding,
                row,
                recommendation
            )

    def analyze_database_status(self):

        rows = (
            self.data
            .get("stability", {})
            .get("database_status", [])
        )

        if not rows:
            return

        for row in rows:

            status = str(
                row.get("status", "")
            ).upper()

            if status not in ("OPEN", "READ WRITE"):
                continue

            self.add_finding(
                "CRITICAL",
                (
                    f"Database status requires attention: "
                    f"{status}."
                ),
                row,
                (
                    "Review the database state and determine "
                    "whether the current status is expected. "
                    "Validate application availability and "
                    "database health before taking corrective action."
                )
            )

    def analyze_archive_log(self):

        rows = (
            self.data
            .get("stability", {})
            .get("archive_log", [])
        )

        if not rows:
            return

        for row in rows:
            evidence = row.copy()

            self.add_finding(
                "INFO",
                "Archive log activity requires review.",
                evidence,
                (
                    "Review archive destination capacity, archive "
                    "generation rate and backup/archive processes "
                    "when investigating recovery or space-related issues."
                )
            )

    def analyze_redo(self):

        rows = (
            self.data
            .get("stability", {})
            .get("redo", [])
        )

        if not rows:
            return

        for row in rows:
            evidence = row.copy()

            self.add_finding(
                "INFO",
                "Redo configuration or activity detected.",
                evidence,
                (
                    "Review redo generation and log switch activity "
                    "when investigating database throughput, "
                    "checkpoint activity or recovery performance."
                )
            )

    def analyze(self):

        self.findings = []

        self.analyze_blocking_sessions()
        self.analyze_long_transactions()
        self.analyze_invalid_objects()
        self.analyze_recovery_area()
        self.analyze_database_status()
        self.analyze_archive_log()
        self.analyze_redo()

        return self.findings