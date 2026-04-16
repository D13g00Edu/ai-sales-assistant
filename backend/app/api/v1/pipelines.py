from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.responses import UploadPipelineResponse
from app.modules.pipelines.services import DatasetPipelineService
from app.core.exceptions import ValidationError

router = APIRouter()

@router.post("", response_model=UploadPipelineResponse)
def upload_dataset(file: UploadFile = File(...)):
    try: return DatasetPipelineService().process_upload(file.file)
    except ValidationError as e: raise HTTPException(422, str(e.errors or e))
    except Exception as e: raise HTTPException(500, str(e))
