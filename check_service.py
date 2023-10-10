import csv
import time
import os

# Function to read the second column of the last row from a CSV file
def get_last_row_second_column_value(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        last_row = None
        for row in reader:
            last_row = row
        if last_row and len(last_row) > 1:
            return last_row[1]  # Second column (index 1) of the last row
        else:
            return None

# Function to update the service status in "service.csv" and delete the old value
def update_service_status(status):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Read the existing data from "service.csv" if it exists
    existing_data = []
    if os.path.exists("service.csv"):
        with open("service.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                existing_data.append(row)

    # Add the current status and time to the data
    existing_data.append([current_time, status])

    # Write the updated data to "service.csv"
    with open("service.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(existing_data)

# Infinite loop to monitor and update the service status
while True:
    # Check the status in "service_status.csv"
    status = get_last_row_second_column_value("service_status.csv")

    if status == "Service Stopped":
        update_service_status("e")
    elif status == "Service Started":
        # Check the status in "service_type.csv" only if the service is started
        service_type = get_last_row_second_column_value("service_type.csv")

        if service_type:
            update_service_status(f"The service is {service_type}.")
        else:
            update_service_status("e")
    else:
        update_service_status("Unknown service status.")
    
    # Sleep for 30 seconds before checking again
    time.sleep(30)
