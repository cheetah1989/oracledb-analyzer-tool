import json

from src.analyzers.stability import StabilityAnalyzer


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

    analyzer = StabilityAnalyzer(
        data=data
    )

    findings = analyzer.analyze()

    print()
    print("Stability Analysis")
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