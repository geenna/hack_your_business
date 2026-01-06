from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    basePath: str
    fileNameDisk: str
    fileNameOriginal: str
    contentType: str

class UserDocumentCreate(DocumentBase):
    pass

class UserDocumentResponse(DocumentBase):
    id: str
    userId: str
    createdAt: datetime
    deletedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProjectDocumentCreate(DocumentBase):
    pass

class ProjectDocumentResponse(DocumentBase):
    id: str
    projectId: str
    createdAt: datetime
    deletedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
