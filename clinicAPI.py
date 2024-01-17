import pandas as pd
import requests as rq
import json


def get_info():
    response = rq.get("https://api.vitaldb.net/cases")
    if response.status_code == 200:
        # Use utf-8-sig encoding to handle the BOM
        data = response.json(encoding="utf-8-sig")
        
        # Now 'data' contains the API response in a Python data structure (probably a dictionary)
        print(data)
    
    else :
        print("not available")

def get_info_using_sheet():
    sheet = pd.read_html("https://docs.google.com/spreadsheets/d/1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY/edit#gid=0")
    print(sheet[0])

def get_info_using_excel(unique_id):
    sheet = pd.read_excel(r"C:\Users\Acer\Desktop\Patient_Dataset.xlsx")
    if unique_id in sheet.iloc[:, 0].values:
            # Extract the row with the specified unique_id
            
            selected_row = sheet[sheet.iloc[:, 0] == unique_id].values.tolist()[0]

            return selected_row
    else:
            print(f"Unique ID '{unique_id}' not found in the specified sheet.")
            return None

print(get_info_using_excel("AA0010"))
    
    
 
