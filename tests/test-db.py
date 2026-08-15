from src.db import get_connection


def main():

    connection = None

    try:
        connection = get_connection()

        print()
        print("Connection test PASSED.")

    except Exception as error:

        print()
        print("Connection test FAILED.")
        print(f"Error: {error}")

    finally:

        if connection:
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()