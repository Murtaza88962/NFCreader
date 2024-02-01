import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
import time

# Function to authenticate with Google Sheets API
def authenticate_google_sheets(creds_path, sheet_name):
    try:
        # Authenticate with Google Sheets API using service account credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        
        # Open the Google Spreadsheet
        sheet = client.open(sheet_name).sheet1  # assuming the sheet is the first sheet in the workbook
        return sheet
    except Exception as e:
        print(f"Error authenticating with Google Sheets API: {e}")
        return None

# Function to get the next patient ID
def get_next_patient_id(sheet):
    try:
        # Find the last row with data
        last_row = len(sheet.col_values(1))

        # If there are no rows in the sheet, start patient ID from 1
        if last_row == 0:
            return 1

        # Get the value of the last patient ID
        last_patient_id = int(sheet.cell(last_row, 1).value)

        # Increment the last patient ID by 1 to get the next patient ID
        next_patient_id = last_patient_id + 1

        return next_patient_id
    except Exception as e:
        print(f"Error getting next patient ID: {e}")
        return None

# Function to fill the web form
def fill_web_form(credentials_path, sheet_name):
    try:
        # Initialize the WebDriver (no need to specify executable_path on macOS)
        driver = webdriver.Chrome()
        
        # URL of the web form
        form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSfivwNiuhFnmH5fSOGI68rlFKyM3PJnR-fYaxDm2DonnBon3g/viewform?pli=1'
        
        # Open the web form
        driver.get(form_url)
        
        # Replace the following XPaths with the actual XPaths of the form fields on the web page
        xpath_mappings = {
            'Name': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'Doctor': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'Latest_apointment_date': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'age': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'gender': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'Glucose': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'BloodPressure': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'Insulin': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'BMI': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'Diagnosed_Diseases': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[10]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'Last_Prescription': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[11]/div/div/div[2]/div/div[1]/div/div[1]/input',
            'New_Prescription': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[12]/div/div/div[2]/div/div[1]/div/div[1]/input'
        }
        
        # Prompt user for patient information
        patient_data = {}
        for field in xpath_mappings.keys():
            value = input(f"Enter {field}: ")
            patient_data[field] = value
        
        # Authenticate with Google Sheets API
        sheet = authenticate_google_sheets(credentials_path, sheet_name)

        # Get the next Patient_id
        next_patient_id = get_next_patient_id(sheet)

        # Add Patient_id to patient_data
        patient_data['Patient_id'] = next_patient_id

        # Fill in the form fields using user input
        for field, xpath in xpath_mappings.items():
            if field in patient_data and patient_data[field] is not None:
                input_field = driver.find_element_by_xpath(xpath)
                input_field.send_keys(str(patient_data[field]))
        
        # Submit the form (replace 'xpath_for_submit_button' with the actual XPath)
        submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        submit_button.click()
        
        # Wait for a few seconds to ensure the form submission is completed
        time.sleep(5)
        
        # Update the Google Sheet with the new data
        if sheet:
            sheet.append_row(list(patient_data.values()))

    except Exception as e:
        print(f"Error filling web form: {e}")

    finally:
        # Close the browser window
        driver.quit()

# Replace these values with your own credentials and sheet name
credentials_path = 'keys.json'
sheet_name = 'Sheet1'

# Call the function to fill the web form using user input
fill_web_form(credentials_path, sheet_name)
