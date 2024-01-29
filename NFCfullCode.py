import asyncio
import websockets
import json
import nfcpy
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Function to authenticate Google Sheets
def authenticate_google_sheets(creds_path, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # assuming the sheet is the first sheet in the workbook
    return sheet

# Function to get patient data from Google Sheets based on patient ID
def get_patient_data_by_id(sheet, patient_id):
    try:
        # Search for the row with the given patient ID
        cell = sheet.find(patient_id)
        if cell:
            row = cell.row
            # Get data from the corresponding row
            data = sheet.row_values(row)
            headers = sheet.row_values(1)  # assuming the first row contains headers
            patient = dict(zip(headers, data))
            return patient
        else:
            print("Patient ID not found.")
            return None
    except Exception as e:
        print(f"Error getting patient data from Google Sheets: {e}")
        return None

async def handle_websocket(websocket, path):
    try:
        # Authenticate Google Sheets
        credentials_path = 'https://docs.google.com/spreadsheets/d/1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY/edit#gid=0'
        sheet_name = 'Sheet1'
        sheet = authenticate_google_sheets(credentials_path, sheet_name)

        # Start NFC reader
        with nfcpy.ContactlessFrontend('usb') as clf:
            print("NFC reader connected.")
            while True:
                # Wait for NFC card to be touched
                tag = clf.connect(rdwr={'on-connect': lambda tag: False})

                # Extract patient ID from NFC card (assuming patient ID is stored as string)
                patient_id = tag.identifier.hex()

                # Get patient data from Google Sheets based on patient ID
                patient_data = get_patient_data_by_id(sheet, patient_id)

                # Send patient data to the client
                if patient_data:
                    await websocket.send(json.dumps(patient_data))
                else:
                    await websocket.send(json.dumps({"error": "Patient ID not found."}))

    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed.")

if __name__ == "__main__":
    start_server = websockets.serve(handle_websocket, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
