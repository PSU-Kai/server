#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.etree import ElementTree as ET
import csv
import os
from datetime import datetime

HOST_NAME = '127.0.0.1'
PORT = 8080
DATA_DIR = '/home/sonali'  # Directory where user profile CSV files will be stored

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(201)
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode("utf-8")
        
        # Parse the incoming XML data
        try:
            root = ET.fromstring(data)
            order_id = root.find('Id').text
            customer = root.find('Customer').text
            interval = float(root.find('Interval').text)
            duration = float(root.find('Duration').text)
            power = float(root.find('Power').text)
            energy_take = float(root.find('EnergyTake').text)
            
            # Get the current timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create a user profile dictionary for the customer
            user_profile = {
                "Timestamp": current_time,
                "Order ID": order_id,
                "Customer": customer,
                "Interval": interval,
                "Duration": duration,
                "Power": power,
                "EnergyTake": energy_take,
            }
            
            # Write the data to the customer's CSV file
            customer_csv_file = os.path.join(DATA_DIR, f"{customer}.csv")
            with open(customer_csv_file, 'a', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=user_profile.keys())
                
                # If the file is empty, write the header row
                if os.path.getsize(customer_csv_file) == 0:
                    csv_writer.writeheader()
                
                csv_writer.writerow(user_profile)
                
            # Print received data
            print(f"Received Order ID: {order_id}")
            print(f"Received Customer: {customer}")
            print(f"Received Interval: {interval}")
            print(f"Received Duration: {duration}")
            print(f"Received Power: {power}")
            print(f"Received EnergyTake: {energy_take}")
            print(f"Received Timestamp: {current_time}")
            
            # Check if the received message is a service message and print it
            message_element = root.find('message')
            if message_element is not None:
                service_message = message_element.text
                print(f"Received Service Message: {service_message}")
                
                # Check if the service message is "Do Service" and the service.csv file exists
                if service_message == "Start Service?":
                    service_csv_file = os.path.join(DATA_DIR, 'GSP.csv')
                    if os.path.exists(service_csv_file):
                        last_row = self.get_last_row_from_csv(service_csv_file)
                        if len(last_row) >= 3:
                            service_status = last_row[2]  # 2nd column (Service Status)
                            service_type = last_row[1]    # 3rd column (Service Type)
                            
                            # Create and send a response for service status
                            response_status = f"Service Status: {service_status}"
                            response = f"<Response>{response_status}</Response>"
                            
                            self.send_response(200)
                            self.send_header("Content-type", "text/xml")
                            self.send_header("Content-length", str(len(response)))
                            self.end_headers()
                            self.wfile.write(response.encode("utf-8"))
                            print(f"Sent Response: {response_status}")
                            
                            # Create and send a response for service type
                            response_type = f"Service Type: {service_type}"
                            response = f"<Response>{response_type}</Response>"
                            
                            self.send_response(200)
                            self.send_header("Content-type", "text/xml")
                            self.send_header("Content-length", str(len(response)))
                            self.end_headers()
                            self.wfile.write(response.encode("utf-8"))
                            print(f"Sent Response: {response_type}")
                            return  # Exit the method after sending both responses
                        else:
                            print("Service.csv does not contain enough columns")
                    else:
                        print("Service.csv does not exist.")
                
        except Exception as e:
            print(f"Error parsing XML: {str(e)}")

    def get_last_row_from_csv(self, file_path):
        try:
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)
                if len(rows) > 0:
                    return rows[-1]  # Get the last row
                else:
                    return []
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return []

if __name__ == "__main__":
    # Ensure the data directory exists and create it if it doesn't
    os.makedirs(DATA_DIR, exist_ok=True)
    
    server = HTTPServer((HOST_NAME, PORT), Handler)
    print(f"Server started on http://{HOST_NAME}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
