import pandas as pd
import requests as rq
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


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

def fill_web_form(patient_data):
    # Set the path to your webdriver executable (e.g., chromedriver.exe)
    driver_path = '/path/to/chromedriver'
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(executable_path=driver_path)
    
    # URL of the web form
    form_url = 'https://example.com/form'
    
    try:
        # Open the web form
        driver.get(form_url)
        
        # Replace the following XPaths with the actual XPaths of the form fields on the web page
        xpath_mappings = {
            'Patient_id': 'xpath_for_patient_id',
            'Name': 'xpath_for_name',
            'Doctor': 'xpath_for_doctor',
            'Latest_apointment_date': 'xpath_for_appointment_date',
            'age': 'xpath_for_age',
            'gender': 'xpath_for_gender',
            'Glucose': 'xpath_for_glucose',
            'BloodPressure': 'xpath_for_blood_pressure',
            'Insulin': 'xpath_for_insulin',
            'BMI': 'xpath_for_bmi',
            'Diagnosed_Diseases': 'xpath_for_diagnosed_diseases',
            'Last_Prescription': 'xpath_for_last_prescription',
            'New_Prescription': 'xpath_for_new_prescription'
        }
        
        # Fill in the form fields
        for field, xpath in xpath_mappings.items():
            if field in patient_data and patient_data[field] is not None:
                input_field = driver.find_element_by_xpath(xpath)
                input_field.send_keys(str(patient_data[field]))
        
        # Submit the form (replace 'xpath_for_submit_button' with the actual XPath)
        submit_button = driver.find_element_by_xpath('xpath_for_submit_button')
        submit_button.click()
        
        # Wait for a few seconds to ensure the form submission is completed
        time.sleep(5)
    
    finally:
        # Close the browser window
        driver.quit()


patient_data_dict = {field: value for field, value in zip(xpath_mappings.keys(), patient_data)}
    
    
 
