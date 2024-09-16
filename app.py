import time
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
import mysql.connector
from mysql.connector import Error

# Set up logging configuration
logging.basicConfig(filename='sheet_monitor.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# MySQL connection configuration (update these placeholders with your actual details)
DB_CONFIG = {
    'user': 'rolwinai',
    'password': 'Rolwin@2003',
    'host': 'localhost',
    'database': 'DATA'
}

def create_mysql_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logging.info("Connected to MySQL database")
            return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

def execute_mysql_query(query, data=None):
    connection = create_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()
            logging.info(f"Executed query: {query}")
        except Error as e:
            logging.error(f"Error executing query: {e}")
        finally:
            cursor.close()
            connection.close()

def create_table_if_not_exists(sheet_name, headers):
    columns = ', '.join([f"`{header}` TEXT" for header in headers])
    query = f"""
    CREATE TABLE IF NOT EXISTS `{sheet_name}` (
        {columns}
    )
    """
    execute_mysql_query(query)

def get_all_sheets(spreadsheet_id, credentials):
    logging.info(f'Fetching all sheets for spreadsheet: {spreadsheet_id}')
    service = build("sheets", "v4", credentials=credentials)
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    logging.info(f'Found sheets: {sheets}')
    return sheets

def get_sheet_data(service, spreadsheet_id, sheet_name):
    logging.info(f'Getting data for sheet: {sheet_name}')
    range_name = f"{sheet_name}!A:Z"  # Adjust the range as needed
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    logging.info(f'Data retrieved for sheet {sheet_name}: {result.get("values", [])}')
    return result.get('values', [])

def read_values(service, spreadsheet_id, range_name):
    logging.info(f'Reading values from range: {range_name}')
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    
    values = result.get('values', [])
    logging.info(f'Values read from range {range_name}: {values}')
    return values

def update_values(service, spreadsheet_id, range_name, values):
    logging.info(f'Updating values in range: {range_name}')
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    logging.info(f'Updated {result.get("updatedCells")} cells.')

def add_values(service, spreadsheet_id, range_name, values):
    logging.info(f'Appending values in range: {range_name}')
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    logging.info(f'Appended {result.get("updates").get("updatedCells")} cells.')

def apply_changes_to_mysql(sheet_name, data):
    connection = create_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Delete existing data
            delete_query = f"DELETE FROM `{sheet_name}`"
            cursor.execute(delete_query)
            logging.info(f"Deleted all rows from table: {sheet_name}")
            
            # Insert new data
            placeholders = ', '.join(['%s'] * len(data[0]))
            insert_query = f"INSERT INTO `{sheet_name}` VALUES ({placeholders})"
            cursor.executemany(insert_query, data)
            connection.commit()
            logging.info(f"Applied changes to table: {sheet_name}")
        except Error as e:
            logging.error(f"Error applying changes to MySQL: {e}")
        finally:
            cursor.close()
            connection.close()

def compare_data(previous_data, current_data):
    changes = []
    prev_set = set(tuple(row) for row in previous_data)
    curr_set = set(tuple(row) for row in current_data)
    
    added_rows = curr_set - prev_set
    removed_rows = prev_set - curr_set
    
    for row in added_rows:
        changes.append(f"Row added: {row}")
    for row in removed_rows:
        changes.append(f"Row removed: {row}")
    
    return changes

def perform_user_operation(service, spreadsheet_id):
    operation = input("What operation do you want to perform? (create/read/update/add): ").lower()
    
    if operation == 'create':
        title = input("Enter the title for the new spreadsheet: ")
        new_spreadsheet_id = create_spreadsheet(service, title)
        print(f"New spreadsheet created with ID: {new_spreadsheet_id}")
    elif operation == 'read':
        range_name = input("Enter the range to read (e.g., Sheet1!A1:B10): ")
        values = read_values(service, spreadsheet_id, range_name)
        print(f"Values read: {values}")
    elif operation == 'update':
        range_name = input("Enter the range to update (e.g., Sheet1!A1:B2): ")
        values = eval(input("Enter the values as a list of lists (e.g., [['A1', 'B1'], ['A2', 'B2']]): "))
        update_values(service, spreadsheet_id, range_name, values)
    elif operation == 'add':
        range_name = input("Enter the range to append to (e.g., Sheet1!A:B): ")
        values = eval(input("Enter the values as a list of lists (e.g., [['New A1', 'New B1'], ['New A2', 'New B2']]): "))
        add_values(service, spreadsheet_id, range_name, values)
    else:
        print("Invalid operation. Please choose create, read, update, or add.")

def monitor_all_sheets(spreadsheet_id, interval=10):
    logging.info(f'Starting to monitor spreadsheet: {spreadsheet_id}')
    credentials = service_account.Credentials.from_service_account_file(
        "key.json", 
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=credentials)
    
    all_sheets = get_all_sheets(spreadsheet_id, credentials)
    previous_data = {}
    
    logging.info("Initial data load and sync...")
    print("Initial data load and sync...")
    
    for sheet in all_sheets:
        sheet_name = sheet['properties']['title']
        headers = get_sheet_data(service, spreadsheet_id, sheet_name)[0]
        create_table_if_not_exists(sheet_name, headers)
        sheet_data = get_sheet_data(service, spreadsheet_id, sheet_name)[1:]
        previous_data[sheet_name] = sheet_data
        apply_changes_to_mysql(sheet_name, sheet_data)
    
    logging.info("Initial sync complete.")
    print("Initial sync complete.")
    
    while True:
        continue_monitoring = input("Do you want to perform manual operations? (Yes/No): ").lower()
        
        if continue_monitoring == 'yes':
            while True:
                perform_user_operation(service, spreadsheet_id)
                continue_operations = input("Do you want to perform another operation? (Yes/No): ").lower()
                if continue_operations != 'yes':
                    break
        
        logging.info("Monitoring for changes...")
        print("Monitoring for changes...")
        
        monitoring_start_time = time.time()
        
        while True:
            time.sleep(interval)
            changes_detected = False
            all_changes = []
            
            for sheet in all_sheets:
                sheet_name = sheet['properties']['title']
                current_data = get_sheet_data(service, spreadsheet_id, sheet_name)[1:]
                
                if current_data != previous_data[sheet_name]:
                    changes = compare_data(previous_data[sheet_name], current_data)
                    if changes:
                        logging.info(f"Changes detected in sheet: {sheet_name}")
                        print(f"\nChanges detected in sheet: {sheet_name}")
                        for change in changes:
                            logging.info(change)
                            print(change)
                        all_changes.extend(changes)
                        changes_detected = True
                    previous_data[sheet_name] = current_data
            
            if all_changes:
                apply_changes_to_mysql(sheet_name, current_data)
            
            if not changes_detected:
                logging.info("No changes detected.")
                print("No changes detected.")
            
            monitoring_end_time = time.time()
            elapsed_time = monitoring_end_time - monitoring_start_time
            logging.info(f"Monitoring elapsed time: {elapsed_time} seconds")
            print(f"Monitoring elapsed time: {elapsed_time} seconds")

if __name__ == "__main__":
    SPREADSHEET_ID = '1KeyEaVNt-LK-Fu68bCmc8sHLdkne52Qwb7GIunDq5jQ'  # Replace with your Google Sheet ID
    monitor_all_sheets(SPREADSHEET_ID)
