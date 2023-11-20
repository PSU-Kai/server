import datetime
import csv
import time

def main():
    # Get the current time
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Ask the operator if they want to do a service
    service_needed = input("Do you want to do a service? (yes/no): ").strip().lower()

    if service_needed == "yes":
        try:
            # Ask the operator about the type of service
            service_type = input("What kind of service would you like? (Shed = S/LoadUp = L/GridEmergency = G/CriticalPeakEvent = C): ").strip().lower()
            if service_type not in ["S", "L", "G", "C"]:
                print("Invalid service type. Please choose from the available options.")
                return

            # If the operator wants to do a service, ask for the number of hours
            hours = float(input("How many hours do you want to allocate for the service?: "))
            if hours < 0:
                print("Please enter a valid positive number of hours.")
            else:
                # Calculate the service end time
                end_time = current_time + datetime.timedelta(hours=hours)
                print(f"You have allocated {hours} hours for {service_type} service.")
                print(f"Service will end at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

                # Create a new CSV file or overwrite existing one
                with open('/home/sonali/GSP.csv', 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(["Start Time", "Service Type", "Status", "End Time", "Allocated Hours", "Chosen Service"])

                    # Write the initial data row
                    csv_writer.writerow([current_time_str, service_type, "Service Started", end_time.strftime('%Y-%m-%d %H:%M:%S'), hours, service_type])

                # Wait for the allocated time to finish or until "Stop" is entered
                while datetime.datetime.now() < end_time:
                    if input("Enter 'Stop' to stop the service: ").strip().lower() == "stop":
                        break
                    time.sleep(1)

                # Mark the service as stopped in the same row
                with open('/home/sonali/GSP.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([current_time_str, service_type, "Service Stopped", "", "", ""])
                print(f"{service_type} service has been stopped.")
        except ValueError:
            print("Invalid input. Please enter a valid number of hours.")
    elif service_needed == "no":
        print("No service will be performed.")
    else:
        print("Invalid response. Please enter 'yes' or 'no.")

if __name__ == "__main__":
    main()
