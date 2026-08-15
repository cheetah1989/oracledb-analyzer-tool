"""
Configuration Analyzer

Evaluates Oracle configuration against configurable rules.
"""

class ConfigurationAnalyzer:

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
            "category": "configuration",
            "finding": finding,
            "evidence": evidence,
            "recommendation": recommendation
        })

    def analyze_processes(self):
        """
        Evaluate PROCESSES and SESSIONS configuration.
        """

        processes = (
            self.data
            .get("configuration", {})
            .get("processes", [])
        )

        for parameter in processes:

            name = parameter.get("name", "").lower()

            if name == "processes":

                value = parameter.get("value")

                if value is None:
                    continue

                try:
                    value = int(value)
                except (ValueError, TypeError):
                    continue

                if value <= 0:
                    continue

                self.add_finding(
                    severity="INFO",
                    finding=(
                        f"Oracle PROCESSES parameter is "
                        f"configured to {value}."
                    ),
                    evidence={
                        "parameter": "processes",
                        "value": value,
                        "isdefault": parameter.get("isdefault"),
                        "ismodified": parameter.get("ismodified")
                    },
                    recommendation=(
                        "Validate the configured process limit "
                        "against peak application concurrency "
                        "and observed session demand."
                    )
                )

            elif name == "sessions":

                value = parameter.get("value")

                if value is None:
                    continue

                try:
                    value = int(value)
                except (ValueError, TypeError):
                    continue

                if value <= 0:
                    continue

                self.add_finding(
                    severity="INFO",
                    finding=(
                        f"Oracle SESSIONS parameter is "
                        f"configured to {value}."
                    ),
                    evidence={
                        "parameter": "sessions",
                        "value": value,
                        "isdefault": parameter.get("isdefault"),
                        "ismodified": parameter.get("ismodified")
                    },
                    recommendation=(
                        "Validate session capacity against "
                        "peak application connection requirements."
                    )
                )

    def analyze_optimizer(self):
        """
        Evaluate selected optimizer parameters.
        """

        optimizer = (
            self.data
            .get("configuration", {})
            .get("optimizer", [])
        )

        rules = self.rules.get("optimizer", {})

        adaptive_plans_rule = rules.get(
            "adaptive_plans", {}
        )

        expected_adaptive_plans = adaptive_plans_rule.get(
            "expected"
        )

        for parameter in optimizer:

            name = parameter.get("name", "").lower()
            value = parameter.get("value")

            if name == "optimizer_adaptive_plans":

                if expected_adaptive_plans is not None:

                    actual = str(value).upper() == "TRUE"

                    expected = bool(
                        expected_adaptive_plans
                    )

                    if actual == expected:

                        self.add_finding(
                            severity="INFO",
                            finding=(
                                "Optimizer adaptive plans "
                                "configuration is aligned "
                                "with the configured baseline."
                            ),
                            evidence={
                                "parameter": name,
                                "value": value,
                                "expected": expected
                            },
                            recommendation="No action required."
                        )

                    else:

                        self.add_finding(
                            severity="WARNING",
                            finding=(
                                "Optimizer adaptive plans "
                                "configuration differs from "
                                "the configured baseline."
                            ),
                            evidence={
                                "parameter": name,
                                "value": value,
                                "expected": expected
                            },
                            recommendation=(
                                "Review the optimizer configuration "
                                "against application workload and "
                                "Oracle upgrade history before changing it."
                            )
                        )

    def analyze_memory(self):
        """
        Report important memory configuration.
        """

        memory = (
            self.data
            .get("configuration", {})
            .get("memory", [])
        )

        for parameter in memory:

            name = parameter.get("name", "").lower()

            if name not in (
                "sga_target",
                "sga_max_size",
                "pga_aggregate_target",
                "memory_target",
                "memory_max_target"
            ):
                continue

            self.add_finding(
                severity="INFO",
                finding=(
                    f"Oracle memory parameter {name} "
                    f"is configured as "
                    f"{parameter.get('display_value')}."
                ),
                evidence={
                    "parameter": name,
                    "value": parameter.get("value"),
                    "display_value": parameter.get(
                        "display_value"
                    ),
                    "isdefault": parameter.get(
                        "isdefault"
                    ),
                    "ismodified": parameter.get(
                        "ismodified"
                    )
                },
                recommendation=(
                    "Review memory configuration against "
                    "available server memory and database workload."
                )
            )

    def analyze(self):

        self.findings = []

        self.analyze_memory()
        self.analyze_processes()
        self.analyze_optimizer()

        return self.findings