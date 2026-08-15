import json

from src.analyzers.storage import StorageAnalyzer


def main():

    # ---------------------------------------------------------
    # Load latest collection
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Storage rules
    # ---------------------------------------------------------

    rules = {
        "tablespace": {
            "critical_percent": 98,
            "warning_percent": 95,
            "info_percent": 85
        },

        "temp": {
            "critical_percent": 95,
            "warning_percent": 85
        },

        "undo": {
            "critical_percent": 95,
            "warning_percent": 85
        }
    }

    # ---------------------------------------------------------
    # Run analyzer
    # ---------------------------------------------------------

    analyzer = StorageAnalyzer(
        data=data,
        rules=rules
    )

    findings = analyzer.analyze()

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print()
    print("Storage Analysis")
    print("================")
    print()

    for finding in findings:

        print(
            f"[{finding['severity']}] "
            f"{finding['finding']}"
        )

        print(
            f"Evidence: "
            f"{finding['evidence']}"
        )

        print(
            f"Recommendation: "
            f"{finding['recommendation']}"
        )

        print()


if __name__ == "__main__":
    main()