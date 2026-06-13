import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class DataLoader:

    STORE_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "store.csv"

    def __init__(self):
        pass

    def load_data(self, data_path):
        logger.info("Loading data from: %s", data_path)
        df = pd.read_csv(data_path, parse_dates=['Date'], low_memory=False)
        logger.info("Loaded %d rows, %d columns", *df.shape)

        logger.info("Loading store data from: %s", self.STORE_DATA_PATH)
        store = pd.read_csv(self.STORE_DATA_PATH)
        logger.info("Store data: %d rows, %d columns", *store.shape)

        pd.set_option('display.max_columns', None)

        logger.info("Merging data with store on 'Store' key (left join)")
        merge_df = df.merge(store, on='Store', how='left')
        logger.info("Merge complete — final shape: %s", merge_df.shape)

        return merge_df
