import json
from pathlib import Path
from datetime import datetime


class JSONWriter:
    """
    Writes collected Oracle environment data to JSON.

    The writer is responsible only for persistence.
    It does not collect data or perform analysis.
    """

    def __init__(self, output_directory="output"):
        self.output_directory = Path(output_directory)

    def write(self, data, database_name):
        """
        Write collected data to a timestamped JSON file.

        Parameters
        ----------
        data : dict
            Collected Oracle environment data.

        database_name : str
            Database name used to organize output.

        Returns
        -------
        Path
            Path to the generated JSON file.
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        database_directory = (
            self.output_directory / database_name
        )

        database_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            database_directory
            / f"environment_{timestamp}.json"
        )

        with output_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                default=str
            )

        return output_file