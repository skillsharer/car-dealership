import os
import urllib.parse
import boto3
from preprocess import preprocess_csv

s3 = boto3.client("s3")
CURATED_BUCKET = os.environ["CURATED_BUCKET"]

def lambda_handler(event, context):
    for record in event["Records"]:
        landing_bucket = record["s3"]["bucket"]["name"]
        raw_key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        if not raw_key.lower().endswith(".csv"):
            print(f"Skipping non-CSV object: {raw_key}")
            continue

        local_input_path = "/tmp/input.csv"
        local_output_path = "/tmp/output.csv"

        print(f"Downloading s3://{landing_bucket}/{raw_key}")
        s3.download_file(
            Bucket=landing_bucket,
            Key=raw_key,
            Filename=local_input_path,
        )

        print("Running preprocessing")
        preprocess_csv(
            input_path=local_input_path,
            output_path=local_output_path,
        )

        output_key = build_output_key(raw_key)

        print(f"Uploading curated file to s3://{CURATED_BUCKET}/{output_key}")
        s3.upload_file(
            Filename=local_output_path,
            Bucket=CURATED_BUCKET,
            Key=output_key,
            ExtraArgs={"ContentType": "text/csv"},
        )

    return {
        "statusCode": 200,
        "message": "Preprocessing completed successfully.",
    }


def build_output_key(raw_key: str) -> str:
    return f"curated/{raw_key}"