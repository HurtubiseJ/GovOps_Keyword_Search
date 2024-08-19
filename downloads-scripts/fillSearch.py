import pandas as pd
import rg_search as rgs
import pyodbc as pdb
import json
from pathlib import Path 

encodings = ['utf-8', 'latin1', 'cp1252']

def try_read_file(file_path, mode='r'):
    for encoding in encodings:
        try:
            with open(file_path, mode, encoding=encoding) as file:
                return file.read(), encoding
        except (UnicodeDecodeError, json.JSONDecodeError): 
            continue
    raise UnicodeDecodeError(f"Unable to decode {file_path} with provided encodings.")

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

def create_DB_cursor():
    try:
        conn = pdb.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        print("Database connection and cursor successfully created.")
        return conn, cursor
    except pdb.Error as e:
        print(f"Failed to connect to database: {e}")
        return None, None
    
CONNECTION_STRING = ("DRIVER={SQL Server};""SERVER=DESKTOP-7H6LSQ4;""DATABASE=LocalGovOp;""TrustedServerConnection=Yes;")
conn, cursor = None, None
conn, cursor = create_DB_cursor()
 
def update_CSV(csv_path):
    df = pd.read_csv(csv_path, encoding='ISO-8859-1', dtype={27: object})
    df = iter_df(df)
    df.to_csv('/home/taco/Desktop/SearchScripts/updated_samCSV.csv')

#Pulls noticeID's from df, run rg_search, fill in found missing values
def iter_df(df):
    numFound = 0 
    checkPercentages(df)
    for i in range(500): #range(len(df)):
        curNoticeID = df.loc[i, "NoticeId"]
        cur_filepath = "/media/taco/5f19c918-24f3-4b20-ba46-1944478d6497/DocumentDownloads/" + curNoticeID
        #Find which rows are Nan
        deselectParam = ['PreferredClientsCustomers', "ProjectLocations", "DEP", "SC", "ContractVehicles", "SES"]
        for col in df.columns:
            if not pd.isnull(df.loc[i, col]):
                deselectParam.append(col)

        download_path = Path('/media/taco/5f19c918-24f3-4b20-ba46-1944478d6497/DocumentDownloads/')
        status_json_path = download_path / 'status.json'

        #load status
        try:
            status_data, _ = load_status(status_json_path)
            if curNoticeID in status_data:
                if status_data[curNoticeID]["parsed"]:
                    print('NoticeID {curNoticeID} already parsed.')
                    continue

            try: 
                text, search_list = rgs.run_rg_search(deselectParam, cur_filepath)
                split_text = text.split('--')
                if split_text == ['']:
                    continue
                fileObj = rgs.create_AllMatches_JSON(split_text, search_list)
                status_data[curNoticeID].update({'parsed': True})
            except:
                print("Error proccessing NoticeID: "+ curNoticeID)
                continue
        except:
            print('Failed to load/update status for {curNoticeID}.')
            continue

        #update missing vals if found
        for col in df.columns:
            if col not in deselectParam and fileObj.get(col) != None and fileObj.get(col) != []: #df is empty but have info in fileObj
                df.loc[i, col] = fileObj.get(col)[0][0]
                print(col + ":" + df.loc[i, col]) 
                numFound += 1 
        print("Finished processing NoticeID: " + curNoticeID)
            
    print(numFound)
    print('-----------')
    checkPercentages(df)
    return df

def to_db(noticeID, param, value, Description):

    if cursor == None: 
        print("Failed to connect to DB.")
        return

    parameters = (
        noticeID, param, value, Description
    )
    sql_command = """
        EXEC InsertSearchData
            @NoticeId = ?, @Param = ?, @Value = ?, @Description = ?
    """
    cursor.execute(sql_command, parameters)
    conn.commit()

def main():
    SAM_CSV_FILEPATH = r"/home/taco/Documents/samcsvfile.csv"
    update_CSV(SAM_CSV_FILEPATH)
    df = pd.DataFrame()
    iter_df(df)


def checkPercentages(df):
    print((1 - df.count() / len(df)) * 100)

if __name__ == "__main__":
    main()