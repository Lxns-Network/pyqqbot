from pydantic import BaseModel, validator


class GetAppAccessTokenResponse(BaseModel):
    access_token: str
    expires_in: int

    @validator('expires_in')
    def expires_in_validator(cls, v):
        return int(v)


class SendMessageResponse(BaseModel):
    id: str
    timestamp: str


class UploadMediaFileResponse(BaseModel):
    file_uuid: str
    file_info: str
    ttl: int
