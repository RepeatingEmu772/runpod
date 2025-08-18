#!/usr/bin/env python3

import os
import argparse
import boto3 # AWS SDK for Python, used to interact with Runpod S3-compatible APIs

def create_s3_client(region: str, endpoint_url: str):

    # Creates and returns an S3 client configured for Runpod network volume S3-compatible API.
    #
    # Args:
    #   region (str): The Runpod datacenter ID, used as the AWS region
    #                 (e.g., 'ca-qc-1').
    #   endpoint_url (str): The S3 endpoint URL for the specific Runpod datacenter
    #                       (e.g., 'https://ca-qc-1-s3api.runpod.io/').

    # Returns:
    #   boto3.client: An S3 client object, configured for the Runpod S3 API.

    # Retrieve Runpod S3 API key credentials from environment variables.
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # Ensure necessary S3 API key credentials are set in the environment
    if not aws_access_key_id or not aws_secret_access_key:
        raise EnvironmentError(
            "Please set AWS_ACCESS_KEY_ID (with S3 API Key Access Key) and "
            "AWS_SECRET_ACCESS_KEY (with S3 API Key Secret Access Key) environment variables. "
            "These are obtained from 'S3 API Keys' in the Runpod console settings."
        )

    # Initialize and return the S3 client for Runpod's S3-compatible API
    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region, # Corresponds to the Runpod datacenter ID
        endpoint_url=endpoint_url, # Datacenter-specific S3 API endpoint
    )

def put_object(s3_client, bucket_name: str, object_name: str, file_path: str):

    # Uploads a local file to the specified Runpod network volume.
    #
    # Args:
    #   s3_client: The S3 client object (e.g., returned by create_s3_client).
    #   bucket_name (str): The ID of the target Runpod network volume.
    #   object_name (str): The desired file path for the object on the network volume.
    #   file_path (str): The local path to the file (including the filename) that will be uploaded.

    try:
        # Attempt to upload the file to the Runpod network volume.
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Successfully uploaded '{file_path}' to Network Volume '{bucket_name}' as '{object_name}'")
    except Exception as e:
        # Catch any exception during upload, print an error, and re-raise
        print(f"Error uploading file '{file_path}' to Network Volume '{bucket_name}' as '{object_name}': {e}")
        raise

def main():

    # Parses command-line arguments and orchestrates the file upload process
    # to a Runpod network volume.

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Upload a file to a Runpod Network Volume using its S3-compatible API. "
                    "Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars to be set "
                    "with your Runpod S3 API key credentials."
    )
    parser.add_argument(
        "-b", "--bucket",
        required=True,
        help="The ID of your Runpod Network Volume (acts as the S3 bucket name)."
    )
    parser.add_argument(
        "-e", "--endpoint",
        required=True,
        help="The S3 endpoint URL for your Runpod datacenter (e.g., 'https://s3api-DATACENTER.runpod.io/')."
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="The local path to the file to be uploaded."
    )
    parser.add_argument(
        "-o", "--object",
        required=True,
        help="The S3 object key (i.e., the desired file path on the Network Volume)."
    )
    parser.add_argument(
        "-r", "--region",
        required=True,
        help="The Runpod datacenter ID, used as the AWS region (e.g., 'ca-qc-1'). Find this in the Runpod console's Storage section or endpoint URL."
    )

    args = parser.parse_args()

    # Create the S3 client using the parsed arguments, configured for Runpod.
    client = create_s3_client(args.region, args.endpoint)

    # Upload the object to the specified network volume.
    put_object(client, args.bucket, args.object, args.file)

if __name__ == "__main__":
    main()
