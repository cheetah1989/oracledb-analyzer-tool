from src.db import get_connection
from src.sql_loader import SQLLoader
from src.collector import Collector


def main():

    connection = None

    try:

        # Establish Oracle connection.
        connection = get_connection()

        # Create SQL loader.
        sql_loader = SQLLoader("sql")

        # Create generic collector.
        collector = Collector(
            connection,
            sql_loader
        )

        # Execute the external SQL file.
        results = collector.execute(
            "environment",
            "database"
        )

        print()
        print("Collector test PASSED.")
        print()
        print("Results:")
        print("--------------------------------")

        for row in results:
            print(row)

        print("--------------------------------")

    except Exception as error:

        print()
        print("Collector test FAILED.")
        print(f"Error: {error}")

        raise

    finally:

        if connection:
            connection.close()
            print()
            print("Connection closed.")


if __name__ == "__main__":
    main()