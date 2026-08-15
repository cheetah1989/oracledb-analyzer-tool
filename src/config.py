import yaml
from pathlib import Path


def load_config(config_path="config/analyzer.yaml"):
    """
    Load the analyzer configuration from a YAML file.

    Parameters
    ----------
    config_path : str
        Path to the analyzer YAML configuration file.

    Returns
    -------
    dict
        Configuration loaded from YAML.
    """

    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError(
            f"Configuration file is empty: {path}"
        )

    return config
