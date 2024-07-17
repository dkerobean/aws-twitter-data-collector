import json
import boto3
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

LOG_FORMAT = '%(levelname)s %(asctime)s %(module)s %(message)s'
logging.basicConfig(filename="youtube_streams.log",
                    format=LOG_FORMAT,
                    level=logging.DEBUG)

log = logging.getLogger()

# YouTube API credentials
api_key = os.getenv('YOUTUBE_API_KEY')

# AWS credentials and configuration
aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_ACCESS_KEY_SECRET')
aws_region = 'eu-north-1'
kinesis_stream_name = 'youtube_stream'

# AWS Kinesis client setup
kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)


def get_youtube_data(query, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=max_results
        ).execute()

        return search_response.get('items', [])

    except HttpError as e:
        log.error(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []


def send_to_kinesis(data):
    try:
        kinesis_client.put_record(
            StreamName=kinesis_stream_name,
            Data=json.dumps(data),
            PartitionKey='partitionkey'
        )
        log.info("Data sent to Kinesis")
    except Exception as e:
        log.error(f"Error sending data to Kinesis: {e}")


def main():
    keywords = ['AWS', 'Cloud']
    for keyword in keywords:
        youtube_data = get_youtube_data(keyword)
        for item in youtube_data:
            send_to_kinesis(item)


if __name__ == "__main__":
    main()