import json
import boto3
import base64
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'dickson-youtube-stream-data-json'
    file_name = 'youtube_stream_data.json'

    records = []

    for record in event.get('Records', []):
        try:
            # Decode the Kinesis data
            payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            logger.info(f"Decoded payload: {payload}")

            # Check if payload is empty
            if not payload:
                logger.warning("Empty payload received")
                continue

            # Parse the JSON data
            data = json.loads(payload)
            records.append(data)
        except base64.binascii.Error as b64_error:
            logger.error(f"Base64 decoding error: {b64_error}")
            logger.error(f"Record content: {record['kinesis']['data']}")
        except json.JSONDecodeError as json_error:
            logger.error(f"JSON decode error: {json_error}")
            logger.error(f"Decoded payload: {payload}")
        except KeyError as key_error:
            logger.error(f"KeyError: {key_error}")
            logger.error(f"Record content: {record}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.error(f"Record content: {record}")

    # Save records to S3 if there are any valid records
    if records:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(records))
        logger.info("Data successfully saved to S3")
    else:
        logger.warning("No valid records to save")

    return {
        'statusCode': 200,
        'body': json.dumps('Data processed successfully')
    }