import requests
import json
import pandas as pd
from datetime import datetime

#function names should be self explanatory
class FictionalLicenseAuthority:
    def __init__(self):
        self.base_url = "http://localhost:30000/drivers-licenses/list?length=150"

    def fetch_data(self, length=150):
        url=self.base_url
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch the data. (Status code: {response.status_code})")
            return []
        
    def list_suspended_licenses(self, data):
        suspended_licenses = [license for license in data if license["suspendat"]]
        return suspended_licenses

    def extract_valid_licenses(self, data):
        today = datetime.today() #.strftime("%d/%m/%Y")
        valid_licenses = [license for license in data if datetime.strptime(license["dataDeExpirare"], "%d/%m/%Y") >= today]
        print(today)
        return valid_licenses

    def find_license_count_by_category(self, data):
        license_counts = {}
        for license in data:
            category = license["categorie"]
            if category in license_counts:
                license_counts[category] += 1
            else:
                license_counts[category] = 1
        return license_counts

    def execute_operation(self, operation_id):
        data = self.fetch_data()
        if operation_id == 1:
            result = self.list_suspended_licenses(data)
        elif operation_id == 2:
            result = self.extract_valid_licenses(data)
        elif operation_id == 3:
            result = self.find_license_count_by_category(data)
        else:
            print("Invalid operation ID")
            return
        
        self.export_to_excel(result)

    def export_to_excel(self, data):
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame(list(data.items()), columns=["Category", "Count"])
        else:
            print("Invalid data format")
            return
        
        df.to_excel("license_data.xlsx", index=False)
        print("Data exported to license_data.xlsx")

if __name__ == "__main__":
    authority = FictionalLicenseAuthority()
    operation_id = int(input("Enter operation ID (1, 2, or 3): "))
    authority.execute_operation(operation_id)