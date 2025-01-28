import glob
import pandas as pd
import os
import shutil
from scripts.utils.snowflake_utilz import *


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def list_file(folder):
    try:
            path = os.path.join(folder,'/*.xlsx')
            content_file = glob.glob(path)
            return content_file
    except Exception as e:
        print(f"Error listing files in foldef '{folder}': {e}")
    return []

def process_raw_data(conn,engine,row_folder):
    files = list_file(row_folder)
    if files:
        try:
            for file_key in files:
                file_name = os.path.basename(file_key)
               
               
                if file_name.endswith(".xlsx"):
                    df = pd.read_excel(file_key)
                else:
                    logging.warning(f"Unsupported file format: {file_name}")
                    continue
                insert_raw_data(table_name="ecommerce",data_frame=df,connection=conn,engine=engine)
                logging.info(f"Inserted data into table 'ecommerce'.")
        except Exception as e:
            logging.info(f"Error processing file '{file_key}': {e}" )

def move_files_to_archive(raw_folder, archive_folder):
    files = list_file(raw_folder)

    if not files:
        logging.info(f"No files found in the folder: {raw_folder}")
        return
    
    for file_key in files:
        try:
            archive_key = os.path.join(
                archive_folder,
                os.path.basename(file_key)
            )

            os.makedirs(os.path.dirname(archive_key),exist_ok=True)

            shutil.move(file_key,archive_key)
            logging.info(f"Successfully moved file '{file_key}' to '{archive_key}'.")
        except Exception as e :
            logging.info(f"error while moving file {file_key}")