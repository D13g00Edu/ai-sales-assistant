from pydantic import BaseModel
class AskRequest(BaseModel):
    question: str
    dataset_id: str = 'default_sales'