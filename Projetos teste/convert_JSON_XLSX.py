import json
import pandas as pd
import os

# Load JSON data from the response.json file
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, 'response.json')

with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access the list of items inside the "data" key
items = data.get("data", [])

# Extract the relevant fields and organize them into a list of dictionaries
extracted_data = []
for item in items:
    if isinstance(item, dict):  # Check item is a dictionary
        # Extract main fields
        row = {
            "sku": item.get("sku"),
            "description": item.get("description"),
            "current_stock": item.get("current_stock"),
            "reserved_stock": item.get("reserved_stock"),
            "real_stock": item.get("real_stock"),
            "minimum_stock_alert": item.get("minimum_stock_alert"),
            # Extract nested company fields
            "company_id": item.get("company", {}).get("id"),
            "company_code": item.get("company", {}).get("code"),
            "company_name": item.get("company", {}).get("name"),
        }
        extracted_data.append(row)

# Create a DataFrame from the extracted data
df = pd.DataFrame(extracted_data)

# Save the DataFrame to an Excel file
excel_file_path = os.path.join(script_dir, 'response.xlsx')
df.to_excel(excel_file_path, index=False)

print(f"Data successfully saved to {excel_file_path}")
