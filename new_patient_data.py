from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_google_sheets(creds_path, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # assuming the sheet is the first sheet in the workbook
    return sheet

def get_next_patient_id(sheet):
    try:
        # Get the last used row in the spreadsheet
        last_row = len(sheet.get_all_values())
        # Increment the last Patient_id and return
        return str(int(sheet.cell(last_row, 1).value) + 1)
    except Exception as e:
        print(f"Error getting next Patient_id: {e}")
        return None

def fill_web_form():
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
        
        # Prompt user for patient information
        patient_data = {}
        for field in xpath_mappings.keys():
            value = input(f"Enter {field}: ")
            patient_data[field] = value
        
        # Get the next Patient_id
        sheet = authenticate_google_sheets(credentials_path, sheet_name)
        patient_data['Patient_id'] = get_next_patient_id(sheet)
        
        # Fill in the form fields using user input
        for field, xpath in xpath_mappings.items():
            if field in patient_data and patient_data[field] is not None:
                input_field = driver.find_element_by_xpath(xpath)
                input_field.send_keys(str(patient_data[field]))
        
        # Submit the form (replace 'xpath_for_submit_button' with the actual XPath)
        submit_button = driver.find_element_by_xpath('xpath_for_submit_button')
        submit_button.click()
        
        # Wait for a few seconds to ensure the form submission is completed
        time.sleep(5)
        
        # Update the Google Sheet with the new data
        sheet.append_row(list(patient_data.values()))

    except Exception as e:
        print(f"Error filling web form: {e}")

    finally:
        # Close the browser window
        driver.quit()

# Replace these values with your own credentials and sheet name
credentials_path = 'path/to/your/credentials.json'
sheet_name = 'YourSheetName'

# Call the function to fill the web form using user input
fill_web_form()
