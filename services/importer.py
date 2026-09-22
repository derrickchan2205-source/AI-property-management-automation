import logging
import pandas as pd

def load_csv(file_path):
    try:
        dataframe = pd.read_csv(file_path)
        logging.info("Loaded file successfully: %s", file_path)
        return dataframe
    except FileNotFoundError:
        logging.exception("Input file not found: %s", file_path)
        raise
    except pd.errors.EmptyDataError:
        logging.exception("Input file is empty: %s", file_path)
        raise