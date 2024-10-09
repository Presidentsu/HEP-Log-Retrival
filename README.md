# Implementation Guide for Log Retrieval Tool

## Overview

This document provides a step-by-step guide to implement and use the Log Retrieval Tool. The tool allows customers to extract logs from the Check Point Infinity Events API using a Python script. The only required inputs are the Client ID, API key, and a time frame for the logs (start date & time, end date & time).

> ### PS
> This script "script2.py" currently is hard-coded with URI respective to EU portal infinity events.
>
> If you want to implement the same for US/AU portal you can simply edit & replace the respective URI as per [CP API documentation here](https://app.swaggerhub.com/apis-docs/Check-Point/infinity-events-api/1.0.0#/Search%20Event%20Logs/logsQuery)
>
> Hopefully next version of scripts can do auto retirval of logs recursively should be in by next few week.

## Prerequisites
Before using the tool, ensure you have the following:

1. Python 3.7+ installed on your system.
2. Access to Client ID and API Key provided by your Check Point account.
3. Basic familiarity with command-line operations.

## Installation
### Clone the Repository:

```
    git clone https://github.com/your-repo/log-retrieval-tool.git
    cd log-retrieval-tool
```
### Install Required Packages:

Make sure to install the required Python packages using the requirements.txt:
```
    pip install -r requirements.txt
    Environment Setup:
```

#### Ensure the Python script (log_retrieval.py) is in your working directory.
#### Usage
Running the Script

1. Run the Script:

      Execute the following command in the terminal:
```
      python log_retrieval.py
```

2. Provide Input:

    The script will prompt you for the following details:


    Client ID: Your Check Point Client ID.

    API Key: Your Check Point API Key.

    Start Time: The start time for log retrieval in ```YYYY-MM-DDTHH:MM:SSZ format```.

    End Time: The end time for log retrieval in ```YYYY-MM-DDTHH:MM:SSZ format```.

3. Retrieve Logs:
    The script will:

    Authenticate using the provided credentials.

    Create a log retrieval task and poll for the task's status.

    Once the task is ready, retrieve logs and save them to a file named log.txt in the working directory.

Example
Here’s an example of how to enter the start and end times:

```
Enter your Client ID: YOUR_CLIENT_ID
Enter your API key: YOUR_API_KEY
Enter the start time (YYYY-MM-DDTHH:MM:SSZ): 2024-09-01T00:00:00Z
Enter the end time (YYYY-MM-DDTHH:MM:SSZ): 2024-09-30T23:59:59Z
```

Output
#### The retrieved logs will be saved in log.txt in JSON format, making it easy to parse and analyze.

## Troubleshooting
### Bearer Token Retrieval Issue:
  
  1. Ensure that the Client ID and API Key are correct and valid.
  
  2. Check if the Check Point API service is accessible from your network.
  
  3. Log Retrieval Task Stuck in Processing:

### If the task stays in the "processing" state for too long, verify the time frame. Extremely large ranges might take more time.
  
  1. Ensure that the API service is not experiencing downtime.
  
  2. Logs Not Saved:

### Verify that the script has write permissions to the working directory.
  
  1. Ensure that the log.txt file is not open in another program while running the script.
  
  2. Script Structure

##### The script consists of the following functions:

```
get_bearer_token(): Authenticates using the Client ID and API Key to retrieve a bearer token.
create_log_task(): Creates a log retrieval task for the specified time frame.
check_task_status(): Polls the task status until it is ready.
retrieve_logs(): Retrieves logs using the task ID and page token.
save_logs_to_file(): Saves the retrieved logs to a file.
```

### Security Considerations

1. Store the Client ID and API Key securely and do not hard-code them into the script.
2. Use a .env file or environment variables to manage sensitive credentials if needed.
3. Restrict access to the log.txt file, as it may contain sensitive information.

## Contact

For further informaiton contact Krishna Sai Marella from Check Point Software Technologies.
