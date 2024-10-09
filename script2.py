import requests
import json
from datetime import datetime
import time

# Function to get a bearer token using the API key
def get_bearer_token(client_id, api_key):
    print("Getting bearer token...")
    url = "https://cloudinfra-gw.portal.checkpoint.com/auth/external"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "clientId": client_id,
        "accessKey": api_key
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Bearer token response status: {response.status_code}")
        if response.status_code == 200:
            token = response.json().get("data", {}).get("token")
            if token:
                print("Bearer token retrieved successfully.")
                return token
            else:
                print("Bearer token not found in response. Full response:", response.text)
                return None
        else:
            print(f"Failed to get bearer token. Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while getting bearer token: {e}")
        return None
# Function to create a task for log retrieval
# Function to create a task for log retrieval
def create_log_task(bearer_token, start_time, end_time):
    print("Creating log retrieval task...")
    url = "https://cloudinfra-gw.portal.checkpoint.com/app/laas-logs-api/api/logs_query"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "cloudService": "Harmony Endpoint",
        "timeframe": {
            "startTime": start_time,
            "endTime": end_time
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Task creation response status: {response.status_code}")
        print(f"Task creation response: {response.text}")
        if response.status_code == 200:
            task_id = response.json().get("data", {}).get("taskId")
            if task_id:
                print(f"Task created successfully. Task ID: {task_id}")
                return task_id
            else:
                print("Task ID not found in the response.")
                return None
        else:
            print(f"Failed to create log task. Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while creating log task: {e}")
        return None


# Function to retrieve logs using taskId and pageToken
# Function to retrieve logs using taskId and pageToken
def retrieve_logs(bearer_token, task_id, page_token):
    print(f"Retrieving logs for task ID: {task_id} with page token: {page_token}")
    url = "https://cloudinfra-gw.portal.checkpoint.com/app/laas-logs-api/api/logs_query/retrieve"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "taskId": task_id,
        "pageToken": page_token
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Log retrieval response status: {response.status_code}")
        if response.status_code == 200:
            # Check if the response contains JSON data
            data = response.json()
            if 'data' in data and 'records' in data['data']:
                records = data['data']['records']
                print(f"Retrieved {len(records)} log records.")
                return records
            else:
                print("No records found in the response data.")
                return None
        else:
            print(f"Failed to retrieve logs. Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving logs: {e}")
        return None

# Function to save logs to a file
def save_logs_to_file(logs):
    print("Saving logs to log.txt...")
    with open("log.txt", "w") as file:
        for log in logs:
            file.write(json.dumps(log, indent=4))
            file.write("\n")
    print("Logs have been saved to log.txt")


# Other functions like `create_log_task` and `check_task_status` remain unchanged...

# Main function to take input and call the relevant functions
# Function to check the status of the log task
# Function to check the status of the log task
def check_task_status(bearer_token, task_id):
    print(f"Checking status of task ID: {task_id}")
    url = f"https://cloudinfra-gw.portal.checkpoint.com/app/laas-logs-api/api/logs_query/{task_id}"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        print(f"Task status response status: {response.status_code}")
        print(f"Task status response: {response.text}")
        if response.status_code == 200:
            data = response.json().get("data", {})
            # Extract pageTokens if state is 'Ready'
            if data.get("state") == "Ready":
                page_tokens = data.get("pageTokens", [])
                if page_tokens:
                    print(f"Page tokens retrieved: {page_tokens}")
                    return page_tokens
                else:
                    print("No page tokens found in the response despite state being 'Ready'.")
                    return None
            else:
                print(f"Task is not ready yet. Current state: {data.get('state')}")
                return None
        elif response.status_code == 404:
            print("Task not yet complete or failed. Status 404 received.")
            return None
        else:
            print(f"Failed to check task status. Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while checking task status: {e}")
        return None


def main():
    # Input from the user
    client_id = input("Enter your Client ID: ")
    api_key = input("Enter your API key: ")
    start_time = input("Enter the start time (YYYY-MM-DDTHH:MM:SSZ): ")
    end_time = input("Enter the end time (YYYY-MM-DDTHH:MM:SSZ): ")

    # Validate date and time format
    try:
        datetime.fromisoformat(start_time.replace('Z', ''))
        datetime.fromisoformat(end_time.replace('Z', ''))
    except ValueError:
        print("Invalid date format. Please use the format 'YYYY-MM-DDTHH:MM:SSZ'.")
        return

    # Step 1: Get Bearer Token
    bearer_token = get_bearer_token(client_id, api_key)
    if not bearer_token:
        return

    # Step 2: Create a task for the logs (assuming the function is available)
    task_id = create_log_task(bearer_token, start_time, end_time)
    if not task_id:
        return

    # Step 3: Check task status until we get a page token or a failure
    print("Checking task status...")
    page_tokens = None
    while not page_tokens:
        page_tokens = check_task_status(bearer_token, task_id)
        if not page_tokens:
            print("Task is still processing. Waiting for 10 seconds before checking again...")
            time.sleep(10)

    # Step 4: Retrieve logs using the pageToken
    logs = []
    for page_token in page_tokens:
        log_data = retrieve_logs(bearer_token, task_id, page_token)
        if log_data:
            logs.append(log_data)

    # Save logs to a file if they were retrieved
    if logs:
        save_logs_to_file(logs)
    else:
        print("No logs were retrieved.")

# Run the script
if __name__ == "__main__":
    main()
