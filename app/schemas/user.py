from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):

    telegram_id: int
    username: str

class UserOut(BaseModel):
    
    id: int
    telegram_id: int
    username: str

    model_config = ConfigDict(from_attributes=True)