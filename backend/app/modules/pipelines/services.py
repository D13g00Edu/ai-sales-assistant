import uuid, pandas as pd
from app.schemas.responses import UploadPipelineResponse
from app.infrastructure.storage import LocalFileStorage
from app.infrastructure.database import DuckDBRepository
from .validators import SchemaValidator
from .transformers import DataTransformer

class DatasetPipelineService:
    def __init__(self):
        self.st, self.db = LocalFileStorage(), DuckDBRepository()
        self.val, self.tr = SchemaValidator(), DataTransformer()

    def process_upload(self, file_stream) -> UploadPipelineResponse:
        did = str(uuid.uuid4())
        raw_path = self.st.save_raw_stream(did, file_stream)
        df_raw = pd.read_excel(raw_path)
        df_val = self.val.validate(df_raw)
        proc_path = self.st.get_processed_filepath(did)
        self.tr.transform_and_export(df_val, proc_path)
        self.db.load_parquet_to_view('ventas', proc_path)
        return UploadPipelineResponse(dataset_id=did, status='processed', rows_processed=len(df_val.dropna(subset=['fecha'])), message='Dataset ingestión exitosa')
