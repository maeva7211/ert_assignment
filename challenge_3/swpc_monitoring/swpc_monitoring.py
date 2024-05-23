"""
Application to monitor data from the NOAA Space
Weather Prediction Center (SWPC) by:
- Requesting and parsing data from the SWPC API
- Writing the data to an InfluxDB bucket
- Visualizing the data using the Influx DB UI dashboard
"""

import datetime
import time

from scheduler import Scheduler

from swpc_monitoring.data_collection import get_data
from swpc_monitoring.data_storage import set_up_influxdb, write_series
from swpc_monitoring.logging import parse_config_ini, setup_logger, initiate_logger

# Read config.ini file and set up logging
config = parse_config_ini()
logger = setup_logger(__name__)
initiate_logger(logger)


class SwpcMonitoring:
    """
    This class handles the parsing of the SWPC API response.
    """

    def __init__(self):
        """Instantiate SwpcMonitoring class."""
        self.setup_run = True
        self.last_timestamp = None

    def workflow(self):
        """Run monitoring workflow."""
        url = config.get("swpc", "data_url_1")
        data = get_data(url)
        if self.setup_run:
            set_up_influxdb()
            self.setup_run = False
        self.last_timestamp = write_series(data, self.last_timestamp)


def main():
    schedule = Scheduler()
    swpc_monitoring = SwpcMonitoring()
    minutes = int(config.get("swpc", "period"))
    schedule.cyclic(datetime.timedelta(minutes=minutes), swpc_monitoring.workflow)
    while True:
        schedule.exec_jobs()
        time.sleep(1)


if __name__ == '__main__':
    main()
