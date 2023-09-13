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
            
        except Exception as e:
            print(f"Error parsing XML: {str(e)}")

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
