import pandas as pd
import requests as rq
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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


def authenticate_google_sheets(creds_path, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # assuming the sheet is the first sheet in the workbook
    return sheet

def get_last_prescription(sheet, patient_id_col, last_prescription_col, patient_id):
    try:
        # Find the row where the patient ID matches
        cell = sheet.find(patient_id)
        # Get the last prescription from the corresponding column
        last_prescription = sheet.cell(cell.row, last_prescription_col).value
        return last_prescription
    except gspread.exceptions.CellNotFound:
        print(f"Patient with ID {patient_id} not found in the sheet.")
        return None

def update_prescription(sheet, patient_id_col, new_prescription_col, patient_id, new_prescription):
    try:
        # Find the row where the patient ID matches
        cell = sheet.find(patient_id)
        # Update the new prescription in the corresponding column
        sheet.update_cell(cell.row, new_prescription_col, new_prescription)
        print("Prescription updated successfully.")
    except gspread.exceptions.CellNotFound:
        print(f"Patient with ID {patient_id} not found in the sheet.")

def main(creds_path, sheet_name, patient_id, doctor_name):
    # Column indices in the Google Sheet (1-based index)
    patient_id_col = 1
    last_prescription_col = 12  # Assuming 'Last_Prescription' is in the 12th column
    new_prescription_col = 13   # Assuming 'New_Prescription' is in the 13th column

    # Authenticate and open the Google Sheet
    sheet = authenticate_google_sheets(creds_path, sheet_name)

    # Get the last prescription
    last_prescription = get_last_prescription(sheet, patient_id_col, last_prescription_col, patient_id)

    if last_prescription is not None:
        print(f"Last Prescription: {last_prescription}")

        # Allow the doctor to write a new prescription
        new_prescription = input("Doctor, enter the new prescription: ")

        # Update the Google Sheet with the new prescription
        update_prescription(sheet, patient_id_col, new_prescription_col, patient_id, new_prescription)

if __name__ == "__main__":
    # Replace these values with your own credentials and sheet name
    credentials_path = 'path/to/your/credentials.json'
    sheet_name = 'YourSheetName'
    
    # Replace these values with the specific patient and doctor information
    patient_id = '123'
    doctor_name = 'Dr. Smith'

    main(credentials_path, sheet_name, patient_id, doctor_name)
    
 
