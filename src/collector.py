class Collector:
    """
    Generic Oracle SQL collector.

    Responsibilities:
        1. Load SQL through SQLLoader.
        2. Execute the SQL against Oracle.
        3. Convert the result into Python dictionaries.

    The collector deliberately does NOT contain:
        - SQL statements
        - Assessment logic
        - Business rules
        - Report formatting

    This keeps the collector reusable for every SQL query
    in the analyzer.
    """

    def __init__(self, connection, sql_loader):
        """
        Initialize the collector.

        Parameters
        ----------
        connection : oracledb.Connection
            Active Oracle database connection.

        sql_loader : SQLLoader
            Object responsible for loading SQL files.
        """

        self.connection = connection
        self.sql_loader = sql_loader

    def execute(self, category, query_name):
        """
        Execute a SQL file and return the results.

        Parameters
        ----------
        category : str
            SQL directory/category.

        query_name : str
            SQL file name without the .sql extension.

        Returns
        -------
        list[dict]
            Query results represented as dictionaries.
        """

        # Load SQL from the external SQL directory.
        sql = self.sql_loader.load(
            category,
            query_name
        )

        with self.connection.cursor() as cursor:

            # Execute the SQL against Oracle.
            cursor.execute(sql)

            # cursor.description contains metadata about
            # the columns returned by the query.
            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            # Retrieve all rows.
            rows = cursor.fetchall()

            # Convert each row into a dictionary.
            results = [
                dict(zip(columns, row))
                for row in rows
            ]

        return results