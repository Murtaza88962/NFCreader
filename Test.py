import gspread
from google.oauth2 import service_account

# Function to authenticate with Google Sheets and return credentials
credentials = None
def authenticate_google_sheets(credentials_path):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    return credentials

# Function to get patient data from Google Sheets based on patient ID
def get_patient_data(sheet, patient_id):
    try:
        # Search for the row with the given patient ID
        cell = sheet.find(patient_id)
        if cell:
            row = cell.row
            # Get data from the corresponding row
            data = sheet.row_values(row)
            headers = sheet.row_values(1)  # assuming the first row contains headers
            patient = dict(zip(headers, data))
            return list(patient.values())  # Return values as a list
        else:
            print("Patient ID not found.")
            return None
    except Exception as e:
        print(f"Error getting patient data from Google Sheets: {e}")
        return None

if __name__ == "__main__":
    # Authenticate Google Sheets
    credentials_path = 'keys.json'   
    credentials = authenticate_google_sheets(credentials_path)
    gc = gspread.authorize(credentials)
    sheet_name = 'Sheet1'
    sheet = gc.open(sheet_name).sheet1

    # Take patient ID as user input
    patient_id = input("Enter patient ID: ")

    # Get patient data from Google Sheets based on user input patient ID
    patient_data = get_patient_data(sheet, patient_id)
    if patient_data:
        print("Patient Data:", patient_data)
