"""
Module that handles collecting data from the
NOAA Space Weather Prediction Center (SWPC).
"""

import json
import requests

from datetime import datetime
from typing import Union

from swpc_monitoring.logging import setup_logger

# Set up logging
logger = setup_logger(__name__)


def get_data(url: str) -> list:
    """
    Get data from SWPC API using provided url.
    """
    logger.info(f"Requesting data from provided url - {url}")
    session = requests.Session()
    with session.get(url, headers=None, stream=True) as resp:
        if not 200 <= resp.status_code <= 299:
            logger.error("Failed to get data. See error below.")
            resp.raise_for_status()
        data = json.loads(resp.text)
        return data


class TimeSerie:
    """
    This class handles the parsing of the SWPC API response.
    """

    def __init__(self, data: list):
        """Instantiate TimeSerie class."""
        self.data = data[1:][::-1]
        self.field_map = {key: ind for ind, key in enumerate(data[0])}

    def reformat_datum(self, data_point: list, field: str) -> Union[int, float, datetime]:
        """Reformat data point based on field type."""
        ind_field = self.field_map[field]
        datum = data_point[ind_field]
        # To do - Figure out how to properly handle None values
        if datum is None:
            return -9999.9999
        if "time" in field:
            return datetime.fromisoformat(datum)
        else:
            return float(datum)
