"""
Storage Analyzer

Analyzes collected Oracle storage information and produces
human-readable findings.

Input:
    Raw collection JSON

Output:
    Standardized findings containing:
        - severity
        - category
        - finding
        - evidence
        - recommendation
"""


class StorageAnalyzer:

    def __init__(self, data, rules):
        """
        Parameters
        ----------
        data : dict
            Raw collected Oracle environment data.

        rules : dict
            Storage assessment thresholds loaded from storage.yaml.
        """

        self.data = data
        self.rules = rules

        self.findings = []

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------

    def add_finding(
        self,
        severity,
        finding,
        evidence,
        recommendation
    ):
        """
        Add a standardized finding.
        """

        self.findings.append({
            "severity": severity,
            "category": "storage",
            "finding": finding,
            "evidence": evidence,
            "recommendation": recommendation
        })

    # ---------------------------------------------------------
    # Tablespace Analysis
    # ---------------------------------------------------------

    def analyze_tablespaces(self):
        """
        Analyze tablespace utilization.
        """

        tablespaces = (
            self.data
            .get("storage", {})
            .get("tablespace_usage", [])
        )

        rule = self.rules.get("tablespace", {})

        critical_threshold = rule.get(
            "critical_percent",
            98
        )

        warning_threshold = rule.get(
            "warning_percent",
            95
        )

        info_threshold = rule.get(
            "info_percent",
            85
        )

        for ts in tablespaces:

            used_percent = ts.get("used_percent")

            if used_percent is None:
                continue

            tablespace_name = ts.get(
                "tablespace_name",
                "UNKNOWN"
            )

            allocated_gb = ts.get(
                "allocated_gb",
                0
            )

            used_gb = ts.get(
                "used_gb",
                0
            )

            free_gb = ts.get(
                "free_gb",
                0
            )

            evidence = {
                "tablespace": tablespace_name,
                "allocated_gb": allocated_gb,
                "used_gb": used_gb,
                "free_gb": free_gb,
                "used_percent": used_percent
            }

            # CRITICAL
            if used_percent >= critical_threshold:

                self.add_finding(
                    severity="CRITICAL",

                    finding=(
                        f"Tablespace {tablespace_name} "
                        f"is critically utilized at "
                        f"{used_percent:.2f}%."
                    ),

                    evidence=evidence,

                    recommendation=(
                        "Increase tablespace capacity before "
                        "free space is exhausted. Review data "
                        "growth and datafile autoextend configuration."
                    )
                )

            # WARNING
            elif used_percent >= warning_threshold:

                self.add_finding(
                    severity="WARNING",

                    finding=(
                        f"Tablespace {tablespace_name} "
                        f"is highly utilized at "
                        f"{used_percent:.2f}%."
                    ),

                    evidence=evidence,

                    recommendation=(
                        "Review tablespace growth and available "
                        "capacity. Plan additional storage before "
                        "the tablespace reaches critical utilization."
                    )
                )

            # INFO
            elif used_percent >= info_threshold:

                self.add_finding(
                    severity="INFO",

                    finding=(
                        f"Tablespace {tablespace_name} "
                        f"has elevated utilization "
                        f"at {used_percent:.2f}%."
                    ),

                    evidence=evidence,

                    recommendation=(
                        "Monitor growth and plan capacity if "
                        "the current growth trend continues."
                    )
                )

    # ---------------------------------------------------------
    # TEMP Analysis
    # ---------------------------------------------------------

    def analyze_temp(self):

        temp_usage = (
            self.data
            .get("storage", {})
            .get("temp_usage", [])
        )

        rule = self.rules.get("temp", {})

        critical_threshold = rule.get(
            "critical_percent",
            95
        )

        warning_threshold = rule.get(
            "warning_percent",
            85
        )

        for temp in temp_usage:

            allocated_gb = temp.get(
                "allocated_gb"
            )

            used_gb = temp.get(
                "used_gb"
            )

            if not allocated_gb or not used_gb:
                continue

            used_percent = (
                 used_gb / allocated_gb
            ) * 100

            tablespace_name = temp.get(
                "tablespace_name",
                "TEMP"
            )

            evidence = {
                "tablespace": tablespace_name,
                "allocated_gb": allocated_gb,
                "used_gb": used_gb,
                "used_percent": round(
                    used_percent,
                    2
                )
            }

            if used_percent >= critical_threshold:

                self.add_finding(
                    "CRITICAL",

                    (
                        f"TEMP tablespace {tablespace_name} "
                        f"is critically utilized at "
                        f"{used_percent:.2f}%."
                    ),

                    evidence,

                    (
                        "Review TEMP-consuming SQL, temporary "
                        "segment usage and TEMP sizing."
                    )
                )

            elif used_percent >= warning_threshold:

                self.add_finding(
                    "WARNING",

                    (
                        f"TEMP tablespace {tablespace_name} "
                        f"has high utilization at "
                        f"{used_percent:.2f}%."
                    ),

                    evidence,

                    (
                        "Review SQL generating large sorts, "
                        "hash operations or temporary segments."
                    )
                )

    # ---------------------------------------------------------
    # UNDO Analysis
    # ---------------------------------------------------------

    def analyze_undo(self):

        undo_usage = (
            self.data
            .get("storage", {})
            .get("undo_usage", [])
        )

        rule = self.rules.get("undo", {})

        critical_threshold = rule.get(
            "critical_percent",
            95
        )

        warning_threshold = rule.get(
            "warning_percent",
            85
        )

        for undo in undo_usage:

            used_percent = undo.get(
                "used_percent"
            )

            if used_percent is None:
                continue

            tablespace_name = undo.get(
                "tablespace_name",
                "UNDO"
            )

            evidence = {
                "tablespace": tablespace_name,
                "allocated_gb": undo.get(
                    "allocated_gb"
                ),
                "used_gb": undo.get(
                    "used_gb"
                ),
                "free_gb": undo.get(
                    "free_gb"
                ),
                "used_percent": used_percent
            }

            if used_percent >= critical_threshold:

                self.add_finding(
                    "CRITICAL",

                    (
                        f"UNDO tablespace {tablespace_name} "
                        f"is critically utilized at "
                        f"{used_percent:.2f}%."
                    ),

                    evidence,

                    (
                        "Investigate long-running transactions "
                        "and increase UNDO capacity if required."
                    )
                )

            elif used_percent >= warning_threshold:

                self.add_finding(
                    "WARNING",

                    (
                        f"UNDO tablespace {tablespace_name} "
                        f"has high utilization at "
                        f"{used_percent:.2f}%."
                    ),

                    evidence,

                    (
                        "Review long-running transactions, "
                        "UNDO retention and workload patterns."
                    )
                )

    # ---------------------------------------------------------
    # Run Analyzer
    # ---------------------------------------------------------

    def analyze(self):

        self.findings = []

        self.analyze_tablespaces()
        self.analyze_temp()
        self.analyze_undo()

        return self.findings