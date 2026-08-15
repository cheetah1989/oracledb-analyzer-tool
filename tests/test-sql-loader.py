from src.sql_loader import SQLLoader


def main():

    loader = SQLLoader("sql")

    sql = loader.load(
        "environment",
        "database"
    )

    print("SQL loaded successfully.")
    print()
    print("SQL:")
    print("--------------------------------")
    print(sql)
    print("--------------------------------")


if __name__ == "__main__":
    main()