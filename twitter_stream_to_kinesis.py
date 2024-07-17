import tweepy
import json
import boto3
from dotenv import load_dotenv
import os

# Twitter API credentials
consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# AWS credentials and configuration
aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS__ACCESS_KEY_SECRET')
aws_region = 'eu-north-1'
kinesis_stream_name = 'twitter_stream'

# Tweepy setup
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# AWS Kinesis client setup
kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

class StreamListener(tweepy.StreamListener):
    def on_data(self, data):
        try:
            kinesis_client.put_record(
                StreamName=kinesis_stream_name,
                Data=json.dumps(data),
                PartitionKey='partitionkey'
            )
        except Exception as e:
            print(f"Error sending data to Kinesis: {e}")
        return True

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        return True

# Stream setup
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# Start streaming tweets containing specific keywords
keywords = ['AWS', 'Cloud', 'Data']
stream.filter(track=keywords)