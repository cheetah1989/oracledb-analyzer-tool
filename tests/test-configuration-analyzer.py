import json

from src.analyzers.configuration import ConfigurationAnalyzer


def main():

    file_path = (
        "output/DEV5CDB/"
        "environment_20260814_202457.json"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    rules = {
        "optimizer": {
            "adaptive_plans": {
                "expected": True
            }
        }
    }

    analyzer = ConfigurationAnalyzer(
        data=data,
        rules=rules
    )

    findings = analyzer.analyze()

    print()
    print("Configuration Analysis")
    print("======================")
    print()

    for finding in findings:

        print(
            f"[{finding['severity']}] "
            f"{finding['finding']}"
        )

        print(
            f"Evidence: {finding['evidence']}"
        )

        print(
            f"Recommendation: "
            f"{finding['recommendation']}"
        )

        print()


if __name__ == "__main__":
    main()