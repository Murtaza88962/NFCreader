import gspread
from oauth2client.service_account import ServiceAccountCredentials

def fetch_patient_data(credentials_file, spreadsheet_id, patient_id):
    try:
        # Authenticate with Google Sheets API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        gc = gspread.authorize(credentials)

        # Open the Google Spreadsheet
        sheet = gc.open_by_key(spreadsheet_id).sheet1

        # Find row index of the patient ID
        row_index = None
        for index, row in enumerate(sheet.get_all_values()):
            if row and row[0] == patient_id:
                row_index = index + 1
                break

        # If patient ID found, return corresponding data
        if row_index:
            return sheet.row_values(row_index)
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    credentials_file = 'keys.json'  # Path to service account credentials JSON file
    spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'  # Replace with your Google Spreadsheet ID
    patient_id = input("Enter patient ID: ")

    patient_data = fetch_patient_data(credentials_file, spreadsheet_id, patient_id)
    if patient_data:
        print("Patient Data:", patient_data)
    else:
        print("Patient ID not found or error occurred.")
