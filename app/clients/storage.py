import boto3
from botocore.client import Config
from ..core.settings import settings


def get_s3_client():
    if not settings.S3_ENDPOINT:
        return None
    session = boto3.session.Session()
    client = session.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
    )
    return client


# Folder conventions (S3 / bucket prefixes):
# raw/ - original downloaded files
# curated/ - cleaned, merged data
# features/ - feature matrix files
# preds/ - model predictions / forecasts
# backtests/ - backtest outputs and reports
