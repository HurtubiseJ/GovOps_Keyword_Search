import sys
import requests
import pandas as pd
import os
import json
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import re
import warnings
from pathlib import Path
from datetime import datetime
import locale
import hashlib

# Set locale explicitly
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# URL for the CSV file
csv_url = "https://falextracts.s3.amazonaws.com/Contract%20Opportunities/datagov/ContractOpportunitiesFullCSV.csv"
csv_file_path = Path("/home/taco/Documents/samcsvfile.csv")

# Directory for downloading documents
download_path = Path('/media/taco/5f19c918-24f3-4b20-ba46-1944478d6497/DocumentDownloads/')
status_json_path = download_path / 'status.json'
error_log_path = download_path / 'error_log.json'
notice_id_list_path = download_path / 'notice_id_list.json'

# Base URL for SAM API
sam_base_url = "https://sam.gov/api/prod/opps/v3/opportunities/"

# List of encodings to try
encodings = ['utf-8', 'latin1', 'cp1252']

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def convert_date_times(date):
    try: #Date time offset
        try: #date time hours offset
            return datetime.fromisoformat(date).strftime(r'%d/%m/%y %H:%M') 
        except:
            print('No hours available.')
        return datetime.fromisoformat(date).strftime(r'%d/%m/%y')
    except:
        print("Unable to convert date.")
        return date

def try_read_file(file_path, mode='r'):
    for encoding in encodings:
        try:
            with open(file_path, mode, encoding=encoding) as file:
                return file.read(), encoding
        except (UnicodeDecodeError, json.JSONDecodeError): 
            continue
    raise UnicodeDecodeError(f"Unable to decode {file_path} with provided encodings.")

def try_write_file(file_path, data, mode='w'):
    for encoding in encodings:
        try:
            with open(file_path, mode, encoding=encoding) as file:
                file.write(data)
            return encoding
        except UnicodeEncodeError:
            continue
    raise UnicodeEncodeError(f"Unable to encode {file_path} with provided encodings.")

def parse_csv(file_path):
    print("Parsing CSV...", flush=True)
    for encoding in encodings:
        try:
            parsed_data = pd.read_csv(file_path, encoding=encoding, usecols=['NoticeId'])

            #Convert dates
            parsed_data[['PostedDate', 'ArchiveData', 'ResponseDeadLine', 'AwardDate']] = parsed_data[['PostedDate', 'ArchiveData', 'ResponseDeadLine', 'AwardDate']].apply(convert_date_times)

            print(f"CSV parsed successfully with {encoding} encoding.", flush=True)
            return parsed_data
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to parse CSV file {file_path} with provided encodings.")

def validate_csv(file_path):
    print("Validating CSV file...", flush=True)
    try:
        pd.read_csv(file_path, encoding='utf-8', usecols=['NoticeId'])
        print("CSV file validated successfully with utf-8 encoding.", flush=True)
    except UnicodeDecodeError as e:
        print(f"CSV file utf-8 validation failed: {e}", flush=True)
        try:
            pd.read_csv(file_path, encoding='latin1', usecols=['NoticeId'])
            print("CSV file validated successfully with latin1 encoding.", flush=True)
        except UnicodeDecodeError as e2:
            print(f"CSV file latin1 validation failed: {e2}", flush=True)
            raise

def validate_json(response):
    print("Validating JSON response...", flush=True)
    try:
        json_data = response.json()
        json.dumps(json_data, ensure_ascii=False)
        print("JSON response validated successfully.", flush=True)
    except json.JSONDecodeError as e:
        print(f"JSON validation failed: {e}", flush=True)
        raise

def load_status(file_path):
    print(f"Loading status from JSON file: {file_path}", flush=True)
    if file_path.exists():
        try:
            data, encoding = try_read_file(file_path)
            return json.loads(data), encoding
        except UnicodeDecodeError as e:
            print(f"Error loading status JSON: {e}", flush=True)
            raise
    else:
        return {}, 'utf-8'  # Return an empty dictionary if the file doesn't exist

def save_status(status_data, file_path):
    print(f"Saving status to JSON file: {file_path}", flush=True)
    try:
        encoding = try_write_file(file_path, json.dumps(status_data, indent=2, ensure_ascii=False))
        print(f"Status JSON saved with {encoding} encoding.", flush=True)
    except UnicodeEncodeError as e:
        print(f"Error saving status JSON: {e}", flush=True)
        raise

def log_error(error_data, file_path):
    try:
        if file_path.exists():
            data, encoding = try_read_file(file_path, mode='r+')
            existing_data = json.loads(data)
            existing_data.append(error_data)
            try_write_file(file_path, json.dumps(existing_data, indent=2, ensure_ascii=False), mode='w')
        else:
            try_write_file(file_path, json.dumps([error_data], indent=2, ensure_ascii=False), mode='w')
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Error logging error: {e}", flush=True)

def download_file_attachment(attachment, notice_folder):
    download_url = f"https://sam.gov/api/prod/opps/v3/opportunities/resources/files/{attachment['resourceId']}/download?&token="
    sanitized_filename = sanitize_filename(attachment.get('name', 'unknown_attachment'))
    file_path = notice_folder / sanitized_filename

    if file_path.exists() and file_path.stat().st_size == attachment.get('size', 0):
        print(f"{sanitized_filename} already exists with the correct size.", flush=True)
        return {
            'name': attachment.get('name', 'unknown'),
            'type': attachment.get('type', 'unknown'),
            'size': attachment.get('size', 0),
            'datePosted': attachment.get('postedDate', 'unknown'),
            'downloadUrl': download_url,
            'localPath': str(file_path)
        }

    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"{sanitized_filename} downloaded successfully.", flush=True)
        return {
            'name': attachment.get('name', 'unknown'),
            'type': attachment.get('type', 'unknown'),
            'size': attachment.get('size', 0),
            'datePosted': convert_date_times(attachment.get('postedDate', 'unknown')), #Changed to convert dates
            'downloadUrl': download_url,
            'localPath': str(file_path)
        }
    except requests.RequestException as e:
        print(f"Failed to download {sanitized_filename}. The file may no longer be available. Error: {e}", flush=True)
        log_error({'notice_id': attachment.get('notice_id'), 'error': str(e)}, error_log_path)
        return None

def process_notice_id(item, status_data, updated_status):
    notice_id = item['NoticeId']
    if notice_id in status_data:
        if status_data[notice_id]['finalized'] or not status_data[notice_id]['needs_update']:
            return

    notice_folder = download_path / notice_id
    os.makedirs(notice_folder, exist_ok=True)

    try:
        print(f"Processing Notice ID {notice_id}...", flush=True)
        response = requests.get(f"{sam_base_url}{notice_id}/resources")
        response.raise_for_status()

        try:
            validate_json(response)
        except Exception as e:
            log_error({'notice_id': notice_id, 'error': 'JSON validation failed', 'details': str(e)}, error_log_path)
            return

        data_json_path = notice_folder / f"{notice_id}_data.json"
        try:
            encoding = try_write_file(data_json_path, json.dumps(response.json(), indent=2, ensure_ascii=False))
            print(f"Data JSON for {notice_id} saved with {encoding} encoding.", flush=True)
        except UnicodeEncodeError as e:
            print(f"Error saving data JSON for {notice_id}: {e}", flush=True)
            log_error({'notice_id': notice_id, 'error': str(e), 'snippet': response.text[:500]}, error_log_path)
            return

        attachments_data = response.json().get('_embedded', {}).get('opportunityAttachmentList', [])[0].get('attachments', [])
        valid_attachments = []
        all_files_downloaded = True

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            for attachment in attachments_data:
                if attachment['type'] == 'file':
                    futures.append(executor.submit(download_file_attachment, attachment, notice_folder))
                elif attachment['type'] == 'link':
                    print(f"Link attachment found: {attachment.get('description', 'unknown')} - {attachment.get('uri', 'unknown')}", flush=True)
                    # Log the link for future handling
                    valid_attachments.append({
                        'name': attachment.get('description', 'unknown'),
                        'type': attachment.get('type', 'link'),
                        'size': attachment.get('size', 0),
                        'datePosted': convert_date_times(attachment.get('postedDate', 'unknown')),
                        'downloadUrl': attachment.get('uri', 'unknown'),
                        'localPath': None
                    })

            for future in as_completed(futures):
                try:
                    valid_attachment = future.result()
                    if valid_attachment:
                        valid_attachments.append(valid_attachment)
                    else:
                        all_files_downloaded = False
                except Exception as download_error:
                    print(f"Error downloading attachment: {download_error}", flush=True)
                    log_error({'notice_id': notice_id, 'error': str(download_error)}, error_log_path)
                    all_files_downloaded = False

        if valid_attachments:
            try:
                encoding = try_write_file(notice_folder / f"{notice_id}_attachments.json", json.dumps(valid_attachments, indent=2, ensure_ascii=False))
                print(f"Attachments data for {notice_id} saved with {encoding} encoding.", flush=True)
            except UnicodeEncodeError as e:
                print(f"Error saving attachments JSON for {notice_id}: {e}", flush=True)
                log_error({'notice_id': notice_id, 'error': str(e), 'snippet': valid_attachments}, error_log_path)
                return

        if all_files_downloaded and valid_attachments:
            try:
                most_recent_date = max([datetime.fromisoformat(attachment['datePosted'].replace('Z', '+00:00')) for attachment in valid_attachments])
                updated_status[notice_id] = {
                    'finalized': True,
                    'needs_update': False,
                    'fileCount': len([f for f in os.listdir(notice_folder) if not f.endswith('.json')]),
                    'mostRecentDate': most_recent_date.isoformat(),
                    'documents': valid_attachments,
                    'azureBlobStorage': status_data.get(notice_id, {}).get('azureBlobStorage', []),
                    'localUpdates': status_data.get(notice_id, {}).get('localUpdates', []),
                    'geminiSent': status_data.get(notice_id, {}).get('geminiSent', False),
                    'geminiReceived': status_data.get(notice_id, {}).get('geminiReceived', False),
                    'parsed': False
                }
            except ValueError as e:
                print(f"Error processing date for Notice ID {notice_id}: {e}", flush=True)
                log_error({'notice_id': notice_id, 'error': str(e)}, error_log_path)
                updated_status[notice_id] = {'finalized': False, 'needs_update': True}
        else:
            updated_status[notice_id] = {'finalized': False, 'needs_update': True}

    except Exception as error:
        print(f"Error fetching or downloading data for Notice ID {notice_id}: {error}", flush=True)
        log_error({'notice_id': notice_id, 'error': str(error)}, error_log_path)
        updated_status[notice_id] = {'finalized': False, 'needs_update': True}

def save_notice_id_list(notice_ids):
    try:
        encoding = try_write_file(notice_id_list_path, json.dumps(notice_ids, indent=2, ensure_ascii=False))
        print(f"Notice ID list saved with {encoding} encoding.", flush=True)
    except UnicodeEncodeError as e:
        print(f"Error saving Notice ID list: {e}", flush=True)
        raise

def load_notice_id_list():
    if notice_id_list_path.exists():
        try:
            data, encoding = try_read_file(notice_id_list_path)
            return json.loads(data)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"Error loading Notice ID list: {e}", flush=True)
            raise
    return []

def process_csv_and_update_notices():
    try:
        # Download the CSV file
        print("Downloading CSV file...", flush=True)
        response = requests.get(csv_url)
        response.raise_for_status()
        with open(csv_file_path, 'wb') as file:
            file.write(response.content)
        print("CSV file downloaded successfully.", flush=True)

        validate_csv(csv_file_path)  # Validate the CSV file before processing

        parsed_data = parse_csv(csv_file_path)

        header_for_notice_id = 'NoticeId'
        opportunity_data = [{'NoticeId': row[header_for_notice_id], 'url': f"{sam_base_url}{row[header_for_notice_id]}/resources" if row[header_for_notice_id] else 'Notice ID missing'} for _, row in parsed_data.iterrows()]

        os.makedirs(download_path, exist_ok=True)

        status_data, _ = load_status(status_json_path) #Checks json too see if file exisits and returns data if so, {} if empty, _ is encoding type
        updated_status = {}

        notice_id_list = load_notice_id_list()
        remaining_notices = [item for item in opportunity_data if item['NoticeId'] not in notice_id_list]

        with tqdm(total=len(remaining_notices), unit='notices', desc="Processing Notices") as pbar:
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(process_notice_id, item, status_data, updated_status) for item in remaining_notices]
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if result:
                            pbar.update(1)
                    except Exception as error:
                        print(f"Error processing notice: {error}", flush=True)
                        log_error({'notice_id': 'unknown', 'error': str(error)}, error_log_path)
                    finally:
                        if remaining_notices:
                            notice_id_list.append(remaining_notices.pop(0)['NoticeId'])
                            save_notice_id_list(notice_id_list)

        # Apply updates to status_data outside of the iteration
        status_data.update(updated_status)
        save_status(status_data, status_json_path)  # Save to the original path after processing
        print("All operations completed successfully!", flush=True)

    except Exception as error:
        print(f"An error occurred: {error}", flush=True)
        log_error({'notice_id': 'N/A', 'error': str(error)}, error_log_path)

if __name__ == "__main__":
    # Ensure the JSON files are created if they don't exist
    if not status_json_path.exists():
        save_status({}, status_json_path)

    if not error_log_path.exists():
        log_error([], error_log_path)

    if not notice_id_list_path.exists():
        save_notice_id_list([])

    process_csv_and_update_notices()
