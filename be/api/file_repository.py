from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import auth
from ..service.file_repository.LocalFileRepository import LocalFileRepository

router = APIRouter(
    prefix="/file-repository",
    tags=["file-repository"]
)


def get_file_repo():
    return LocalFileRepository(upload_dir="uploads")

@router.post("/upload")
def upload_files(
    files: List[UploadFile] = File(...), 
    user: dict = Depends(auth.get_current_user), # Requires active session
    db: Session = Depends(auth.get_db) # Database connection available as requested
):
    results = []
    try:
        for file in files:
            # Save file using the repository
            # Only using filename for simplicity, assuming no conflicts or overriding is handled/accepted
            file_path = repository.save_file(file, file.filename)
            results.append({
                "filename": file.filename, 
                "path": file_path, 
                "message": "File uploaded successfully"
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
