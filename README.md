

# Real-Time Data Pipeline with AWS

## Overview

This project demonstrates a real-time data pipeline using various AWS services to handle and analyze data from the Youtube API.

## Architecture
![Architecture Diagram](https://drive.google.com/file/d/12mxIDaScKshnkutQb7pbWSrfVDDbCbHO/view?usp=sharing)

1. **Youtube API**: Collects stream data from Youtube.
2. **AWS Kinesis**: Streams data in real-time.
3. **AWS Lambda**: Processes the data and stores it in S3.
4. **AWS S3**: Stores the processed data.
5. **AWS SageMaker**: Analyzes the data for insights.
6. **AWS QuickSight**: Visualizes the analyzed data.

SNS notifications are used to alert on the success or failure of the Lambda function, ensuring smooth operation.

## Setup

1. **Youtube API**: Configure API keys and access for data collection.
2. **AWS Kinesis**: Set up a Kinesis stream to handle real-time data.
3. **AWS Lambda**: Deploy a Lambda function to process data from Kinesis and store it in S3.
4. **AWS S3**: Create an S3 bucket for data storage.
5. **AWS SageMaker**: Configure SageMaker to pull data from S3 and perform analysis.
6. **AWS QuickSight**: Set up QuickSight for data visualization.

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/dkerobean/aws-youtube-data-collector
    cd your-repo
    ```

2. Configure your Twitter API credentials and AWS services.

3. Deploy the Lambda function and set up the Kinesis stream to process incoming data.

4. Set up SNS for notifications on Lambda function success or failure.

5. Configure SageMaker to analyze data from S3 and visualize it using QuickSight.

## Contributions

Feel free to fork the repository, make improvements, and submit pull requests.


