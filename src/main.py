from src.db import get_connection
from src.sql_loader import SQLLoader
from src.collector import Collector
from src.config import load_config
from src.output import JSONWriter
from datetime import datetime


def main():

    print()
    print("Oracle Environment Analyzer")
    print("============================")
    print()

    # ---------------------------------------------------------
    # 1. Load application configuration
    # ---------------------------------------------------------

    config = load_config()

    sql_directory = config["sql_directory"]

    # ---------------------------------------------------------
    # 2. Establish Oracle connection
    # ---------------------------------------------------------

    connection = get_connection()

    try:

        # -----------------------------------------------------
        # 3. Create reusable components
        # -----------------------------------------------------

        sql_loader = SQLLoader(
            sql_directory
        )

        collector = Collector(
            connection,
            sql_loader
        )

        # -----------------------------------------------------
        # 4. Execute configured collections
        # -----------------------------------------------------

        results = {}

        collections = config["collections"]

        for category, queries in collections.items():

            print()
            print(f"Collecting category: {category}")
            print("--------------------------------")

            results[category] = {}

            for query_name in queries:

                print(
                    f"  Collecting: {query_name}"
                )

                query_result = collector.execute(
                    category,
                    query_name
                )

                results[category][query_name] = (
                    query_result
                )

                print(
                    f"  Rows collected: "
                    f"{len(query_result)}"
                )

        # -----------------------------------------------------
        # 5. Display collection summary
        # -----------------------------------------------------

        print()
        print("Collection completed successfully.")
        print()

        for category, queries in results.items():

            print(category)

            for query_name, rows in queries.items():

                print(
                    f"  {query_name}: "
                    f"{len(rows)} rows"
                )

    finally:

        connection.close()

        print()
        print("Oracle connection closed.")

    # -----------------------------------------------------
    # 5. Identify database name
    # -----------------------------------------------------

    database_name = (
        results["environment"]["database"][0]["name"]
    )

    # -----------------------------------------------------
    # 6. Add collection metadata
    # -----------------------------------------------------

    output_data = {
        "metadata": {
            "collection_time": (datetime.now().isoformat()),
            "database": database_name
        },
        **results
    }

    # -----------------------------------------------------
    # 7. Persist collected data
    # -----------------------------------------------------

    writer = JSONWriter(
        config.get("output_directory", "output")
    )

    output_file = writer.write(
        output_data,
        database_name
    )

    print()
    print(
        f"Raw collection saved to: {output_file}"
    )


if __name__ == "__main__":
    main()