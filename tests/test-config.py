from src.config import load_config


def main():
    config = load_config()

    print("Configuration loaded successfully!")
    print()
    print("SQL directory:", config["sql_directory"])
    print()
    print("Collections:")

    for category, queries in config["collections"].items():
        print(f"  {category}:")
        for query in queries:
            print(f"    - {query}")


if __name__ == "__main__":
    main()