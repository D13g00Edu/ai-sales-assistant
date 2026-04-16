import os, shutil
from app.core.config import get_settings

class LocalFileStorage:
    def __init__(self):
        self.s = get_settings()
        os.makedirs(self.s.DATA_RAW_DIR, exist_ok=True)
        os.makedirs(self.s.DATA_PROCESSED_DIR, exist_ok=True)

    def save_raw_stream(self, dataset_id: str, file_stream) -> str:
        fp = os.path.join(self.s.DATA_RAW_DIR, f'{dataset_id}.xlsx')
        with open(fp, 'wb') as f: shutil.copyfileobj(file_stream, f)
        return fp

    def get_processed_filepath(self, dataset_id: str) -> str:
        return os.path.join(self.s.DATA_PROCESSED_DIR, f'{dataset_id}.parquet')
