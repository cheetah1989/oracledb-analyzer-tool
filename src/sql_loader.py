from pathlib import Path

class SQLLoader:
    """
    Loads SQL statements from the external SQL directory.

    The loader is responsible only for locating and reading
    SQL files. It does not execute SQL and does not know
    anything about Oracle database objects.

    Example:

        load("environment", "database")

    loads:

        sql/environment/database.sql
    """

    def __init__(self, sql_directory="sql"):
        self.sql_directory = Path(sql_directory)

    def load(self, category, query_name):
        """
        Load a SQL file.

        Parameters
        ----------
        category : str
            SQL category, for example 'environment'.

        query_name : str
            SQL file name without the .sql extension.

        Returns
        -------
        str
            SQL statement contained in the file.
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

        sql = sql_file.read_text(
            encoding="utf-8"
        ).strip()

        if not sql:
            raise ValueError(
                f"SQL file is empty: {sql_file}"
            )

        return sql