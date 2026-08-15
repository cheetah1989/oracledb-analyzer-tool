import os

import oracledb
from dotenv import load_dotenv

oracledb.init_oracle_client(lib_dir=r"C:/Users/U6080302/oracle/product/21.0.0/client_1/bin")
# Load environment variables from the .env file.
load_dotenv()


def get_connection():
    """
    Create and return an Oracle database connection.

    Database credentials and connection details are read
    from environment variables rather than being hard-coded.

    Requires below parameter to be set to TRUE:
    alter system set sec_case_sensitive_logon = TRUE scope = both;



    Required environment variables:
        ORACLE_USER
        ORACLE_PASSWORD
        ORACLE_DSN

    Returns
    -------
    oracledb.Connection
        An active Oracle database connection.

    Raises
    ------
    ValueError
        If any required environment variable is missing.
    """

    username = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    dsn = os.getenv("ORACLE_DSN")

    # Validate configuration before attempting the connection.
    missing = []

    if not username:
        missing.append("ORACLE_USER")

    if not password:
        missing.append("ORACLE_PASSWORD")

    if not dsn:
        missing.append("ORACLE_DSN")

    if missing:
        raise ValueError(
            "Missing required environment variables: "
            + ", ".join(missing)
        )

    print(f"Connecting to Oracle using DSN: {dsn}")

    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=dsn
    )

    print("Oracle connection successful.")

    return connection