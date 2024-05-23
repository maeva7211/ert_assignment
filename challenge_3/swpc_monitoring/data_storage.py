"""
Module that handles storing data collected from the
NOAA Space Weather Prediction Center (SWPC) to an
Influx database.
"""

import os
import sys

from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import Authorization, Bucket, InfluxDBClient, Permission, PermissionResource, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import Optional

from swpc_monitoring.data_collection import TimeSerie
from swpc_monitoring.logging import parse_config_ini, setup_logger

# Take environment variables from .env
load_dotenv()
# Read config.ini file
config = parse_config_ini()
# Set up logging
logger = setup_logger(__name__)


def create_authorization(permissions: Optional[list] = None) -> Authorization:
    """
    Create a new API token with predefined permissions or with read&write
    permissions to a bucket.
    """
    with InfluxDBClient.from_env_properties() as client:
        authorizations_api = client.authorizations_api()
        description = config.get('swpc', 'api_token_description')
        org_ids = get_organizations_id()
        org_id = org_ids[os.environ.get("INFLUXDB_V2_ORG")]
        # Create Read and Write permissions for the bucket
        if permissions is None:
            buckets_api = client.buckets_api()
            buckets = buckets_api.find_bucket_by_name(config.get('swpc', 'bucket_name'))
            bucket_id = buckets.id
            org_resource = PermissionResource(org_id=org_id, id=bucket_id, type="buckets")
            read = Permission(action="read", resource=org_resource)
            write = Permission(action="write", resource=org_resource)
            permissions = [read, write]
        authorization = Authorization(org_id=org_id, permissions=permissions, description=description)
        request = authorizations_api.create_authorization(authorization=authorization)
    return request


def create_bucket(bucket_name: str, bucket_description: str):
    """
    Create specific InfluxDb bucket.
    """
    logger.info(f"Create InfluxDB bucket '{bucket_name}'.")
    with InfluxDBClient.from_env_properties() as client:
        buckets_api = client.buckets_api()
        buckets_api.create_bucket(bucket_name=bucket_name,
                                  description=bucket_description,
                                  org=client.org)


def create_organization(organization_name: str):
    """
    Create specific organization.
    """
    logger.info(f"Create organization '{organization_name}'.")
    with InfluxDBClient.from_env_properties() as client:
        organizations_api = client.organizations_api()
        organizations_api.create_organization(name=organization_name)


def find_bucket(bucket_name: str) -> Optional[Bucket]:
    """
    Check if specific InfluxDB bucket exists.
    """
    logger.info(f"Check that InfluxDB bucket '{bucket_name}' exists.")
    with InfluxDBClient.from_env_properties() as client:
        buckets_api = client.buckets_api()
        bucket = buckets_api.find_bucket_by_name(bucket_name)
    return bucket


def get_authorizations() -> list:
    """
    Get list of all existing authorizations to interface with InfluxDB.
    """
    with InfluxDBClient.from_env_properties() as client:
        authorizations_api = client.authorizations_api()
        list_authorizations = authorizations_api.find_authorizations()
    return list_authorizations


def get_organizations_id() -> dict:
    """
    Get list of all registered organizations.
    """
    with InfluxDBClient.from_env_properties() as client:
        organizations_api = client.organizations_api()
        organizations = organizations_api.find_organizations()
    return {org.name: org.id for org in organizations}


def get_point(data_point: list, ts: TimeSerie) -> tuple[Point, datetime]:
    """
    Create a point object identified by its measurement, tag
    keys and values, field keys and values, and timestamp.
    """
    timestamp = datetime.now()
    point = Point("space_weather") \
        .tag("Agency", "NOAA") \
        .tag("Satellite", "DSCOVR")
    for key, val in ts.field_map.items():
        if key == "propagated_time_tag":
            continue
        if key == "time_tag":
            timestamp = ts.reformat_datum(data_point, key)  # type: ignore
            point.time(timestamp)
        else:
            field_name = key.capitalize()
            field_val = ts.reformat_datum(data_point, key)
            point.field(field_name, field_val)
    return point, timestamp


def get_series(flux_query: str) -> list:
    """
    Retrieve time serie data from an InfluxDB bucket based on
    provided flux query.
    """
    bucket_name = config.get("swpc", "bucket_name")
    logger.info(f"Query time serie data from InfluxDB bucket '{bucket_name}'.")
    with InfluxDBClient.from_env_properties() as client:
        query_api = client.query_api()
        response = query_api.query(flux_query)
        results = []
        for table in response:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))
        return results


def set_environment_variables():
    """
    Set InfluxDB environment variables required to
    authentificate to the API.
    """
    os.environ["INFLUXDB_V2_URL"] = os.getenv('URL')
    os.environ["INFLUXDB_V2_ORG"] = os.getenv('ORG')
    os.environ["INFLUXDB_V2_TOKEN"] = os.getenv('TOKEN')


def set_up_influxdb(all_access: bool = True):
    """
    Workflow to set up InfluxDB after install.
    """
    set_environment_variables()
    list_authorizations = get_authorizations()
    descriptions = [auth.description for auth in list_authorizations]
    create_auth = True if len(descriptions) == 1 else False
    if create_auth:
        logger.info("Creating API token.")
        if all_access:
            authorization_request = create_authorization(list_authorizations[0].permissions)
        else:
            authorization_request = create_authorization()
        new_token = authorization_request.token
        update_token(new_token)
    else:
        logger.info("API token already created.")


def update_token(token: str):
    """
    Update environment variable with new token value
    after creationg of new API token.
    """
    os.environ["INFLUXDB_V2_TOKEN"] = token


def write_series(data: list, last_timestamp: Optional[datetime]) -> datetime:
    """
    Write a group of points (time series) to an InfluxDB bucket.
    """
    ts = TimeSerie(data)
    bucket_name = config.get("swpc", "bucket_name")
    logger.info(f"Write time serie data to InfluxDB bucket '{bucket_name}'.")
    with InfluxDBClient.from_env_properties() as client:
        with client.write_api(write_options=SYNCHRONOUS) as writer:
            for data_point in ts.data:
                point, current_timestamp = get_point(data_point, ts)
                # Allow for one data point overlap
                if last_timestamp and last_timestamp > current_timestamp:
                    break
                try:
                    writer.write(bucket=bucket_name, record=point)
                except InfluxDBError as e:
                    logger.error(f"Failed to write to InfluxDB bucket '{bucket_name}'. Error: {e}")
                    sys.exit()
            last_timestamp = ts.reformat_datum(ts.data[0], "time_tag")  # type: ignore
            return last_timestamp  # type: ignore
