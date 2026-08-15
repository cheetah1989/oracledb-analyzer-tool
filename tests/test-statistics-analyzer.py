import json

from src.analyzers.statistics import StatisticsAnalyzer


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

    analyzer = StatisticsAnalyzer(
        data=data
    )

    findings = analyzer.analyze()

    print()
    print("Statistics Analysis")
    print("======================")
    print()


    for finding in findings:
        print(
            f"[{finding['severity']}] "
            f"{finding['message']}"
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