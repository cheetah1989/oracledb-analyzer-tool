from pathlib import Path


class SQLLoader:
    """
    Loads SQL statements from the external sql/ directory.

    Keeping SQL outside Python allows DBAs to modify or tune
    collection queries without modifying application code.
    """

    def __init__(self, sql_directory="sql"):
        self.sql_directory = Path(sql_directory)

    def load(self, category, query_name):
        """
        Load a SQL file based on category and query name.

        Example:

            load("environment", "database")

        loads:

            sql/environment/database.sql
        """

        sql_file = (
            self.sql_directory
            / category
            / f"{query_name}.sql"
        )

        if not sql_file.exists():
            raise FileNotFoundError(
                f"SQL file not found: {sql_file}"
            )

        return sql_file.read_text(encoding="utf-8")
