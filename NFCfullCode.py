import asyncio
import websockets
import json
import gspread
from google.oauth2 import service_account
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name='World')

# Function to authenticate with Google Sheets and return credentials
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
            return patient
        else:
            print("Patient ID not found.")
            return None
    except Exception as e:
        print(f"Error getting patient data from Google Sheets: {e}")
        return None

# Function to handle websocket communication
async def handle_websocket(websocket, path):
    try:
        # Authenticate Google Sheets
        credentials_path = 'keys.json'
        credentials = authenticate_google_sheets(credentials_path)
        gc = gspread.authorize(credentials)
        sheet_name = 'Sheet1'
        sheet = gc.open(sheet_name).sheet1

        while True:
            message = await websocket.recv()
            if message == "connect":  # Check if the client wants to connect
                print("WebSocket connection established.")
                continue  # Skip the rest of the loop and wait for another message

            # Get patient data from Google Sheets based on patient ID
            patient_data = get_patient_data(sheet, message)

            # Send patient data to the client
            if patient_data:
                await websocket.send(json.dumps(patient_data))
            else:
                await websocket.send(json.dumps({"error": "Patient ID not found."}))

    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed.")

async def start_servers():
    # Start Flask server
    flask_task = asyncio.to_thread(app.run, debug=True, use_reloader=False, host='localhost', port=5000)

    # Start WebSocket server
    websocket_server_task = websockets.serve(handle_websocket, "localhost", 8765)

    # Run both servers concurrently
    await asyncio.gather(flask_task, websocket_server_task)

if __name__ == "__main__":
    asyncio.run(start_servers())
