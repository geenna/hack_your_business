import os
import uuid
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import auth
from ..persistence.model import UserDocumentModel as user_document_models
from ..persistence.model import ProjectDocumentModel as project_document_models
from ..persistence.model import UserModel as models
router = APIRouter(prefix="/repository", tags=["repository"])
allow_admin_only = auth.RoleChecker(["all"])
allow_user_only = auth.RoleChecker(["user"])
# Base directory to store uploaded files. Files will be organized by userId and then by type.
# Example structure: repository/user/user123/uuid-filename
BASE_STORAGE_PATH = Path(__file__).parent.parent.parent / "repository"    

@router.post("/add-file", response_model=Dict[str, Any])
async def add_file(
    files: List[UploadFile] = File(..., description="The list of files to upload."),
    db: Session = Depends(auth.get_db),
    prefix: str = Query(..., alias="type", description="The category or type of the file (userFile or projectFile)."),
    external_id: str = Query(..., alias="userId", description="The unique identifier of the owner of the file."),
    user: models.User = Depends(allow_user_only)
) -> Dict[str, Any]:
   
    if not files:
        raise HTTPException(status_code=400, detail="No files provided in the upload.")

    # Validate file_type
    if prefix not in ["user", "project"]:
        raise HTTPException(status_code=400, detail=f"Unsupported prefix '{prefix}'.")

    # Construct basePath: file_type + external_id (e.g., "user123" or "project456")
    base_path = f"{prefix}/{external_id}"

    # Construct the target directory path: BASE_STORAGE_PATH / file_type / external_id
    target_directory: Path = BASE_STORAGE_PATH / prefix / external_id
    target_directory.mkdir(parents=True, exist_ok=True)

    # Prepare lists for tracking
    document_records = []
    file_data_list = []  # Store file content and metadata before saving to filesystem

    # First pass: create database records and prepare file data
    for file in files:
        if not file.filename:
            db.rollback()
            raise HTTPException(status_code=400, detail="One or more files have no filename.")

        # Extract file extension from original filename
        file_extension = Path(file.filename).suffix
        
        # Generate UUID for filename on disk and add extension
        file_uuid = str(uuid.uuid4())
        file_name_disk = f"{file_uuid}{file_extension}"

        # Get content type
        content_type = file.content_type or "application/octet-stream"

        # Create document record based on file_type
        if prefix == "user":
            document_record = user_document_models.UserDocument(
                userId=external_id,
                basePath=base_path,
                fileNameDisk=file_name_disk,
                fileNameOriginal=file.filename,
                contentType=content_type
            )
        elif prefix == "project":
            document_record = project_document_models.ProjectDocument(
                projectId=external_id,
                basePath=base_path,
                fileNameDisk=file_name_disk,
                fileNameOriginal=file.filename,
                contentType=content_type
            )
        
        document_records.append(document_record)
        db.add(document_record)

        # Read file content (needs to be done before commit for async files)
        try:
            content = await file.read()
            file_data_list.append({
                "content": content,
                "fileNameDisk": file_name_disk,
                "fileNameOriginal": file.filename
            })
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to read file '{file.filename}': {e}")

    # Commit all database records at once
    try:
        db.commit()
        # Refresh records to get IDs
        for record in document_records:
            db.refresh(record)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save records to database: {e}")

    # Second pass: save files to filesystem (only if DB commit was successful)
    uploaded_files = []
    errors = []

    for file_data in file_data_list:
        file_location: Path = target_directory / file_data["fileNameDisk"]
        try:
            with open(file_location, "wb") as buffer:
                buffer.write(file_data["content"])
            uploaded_files.append(file_data["fileNameOriginal"])
        except Exception as e:
            errors.append(f"Failed to save file '{file_data['fileNameOriginal']}' to filesystem: {e}")
            # Note: DB records are already committed, so we track errors but don't rollback

    if errors and not uploaded_files:
        # If all files failed to save to filesystem, but DB records are saved
        # This is a partial failure scenario
        raise HTTPException(status_code=500, detail=f"Database records created but failed to save files to filesystem: {'; '.join(errors)}")

    response: Dict[str, Any] = {
        "uploaded_files": uploaded_files,
        "document_ids": [str(record.id) for record in document_records]
    }
    if errors:
        response["errors"] = errors

    return response

@router.get("/get-file")
def get_file(
    file_id: str = Query(..., alias="fileId", description="The ID of the document record (from userDocuments or projectDocuments table)."),
    prefix: str = Query(..., alias="type", description="The category or type of the file (user or project)."),
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_user_only)
):
   
    if not file_id:
        raise HTTPException(status_code=400, detail="File ID cannot be empty.")

    # Validate prefix
    if prefix not in ["user", "project"]:
        raise HTTPException(status_code=400, detail=f"Unsupported prefix '{prefix}'.")

    # Find document record in database by ID
    if prefix == "user":
        stmt = select(user_document_models.UserDocument).where(
            user_document_models.UserDocument.id == file_id,
            user_document_models.UserDocument.deletedAt.is_(None)
        )
        document = db.execute(stmt).scalars().first()
    elif prefix == "project":
        stmt = select(project_document_models.ProjectDocument).where(
            project_document_models.ProjectDocument.id == file_id,
            project_document_models.ProjectDocument.deletedAt.is_(None)
        )
        document = db.execute(stmt).scalars().first()

    if not document:
        raise HTTPException(status_code=404, detail=f"File with id '{file_id}' not found in '{prefix}' documents table or already deleted.")

    # Get external_id based on document type
    external_id = document.userId if prefix == "user" else document.projectId

    # Construct file path
    file_path: Path = BASE_STORAGE_PATH / prefix / external_id / document.fileNameDisk

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"File with id '{file_id}' not found in filesystem.")

    # Open file as stream and return with StreamingResponse
    def iterfile():
        with open(file_path, "rb") as file:
            yield from file

    return StreamingResponse(
        iterfile(),
        media_type=document.contentType or "application/octet-stream",
        headers={"Content-Disposition": f'inline; filename="{document.fileNameOriginal}"'}
    )

@router.get("/get-all-files", response_model=List[Dict[str, Any]])
def get_all_files(
    prefix: str = Query(..., alias="prefix", description="The category or type of the file (user or project)."),
    external_id: str = Query(..., alias="id", description="The unique identifier (userId or projectId)."),
    flg_deleted: bool = Query(False, alias="flgDeleted", description="If true, includes deleted files."),
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_admin_only)

) -> List[Dict[str, Any]]:
   
    # Validate prefix
    if prefix not in ["user", "project"]:
        raise HTTPException(status_code=400, detail=f"Unsupported prefix '{prefix}'.")

    # Build query based on prefix
    if prefix == "user":
        stmt = select(user_document_models.UserDocument).where(
            user_document_models.UserDocument.userId == external_id
        )
        if not flg_deleted:
            stmt = stmt.where(user_document_models.UserDocument.deletedAt.is_(None))
    elif prefix == "project":
        stmt = select(project_document_models.ProjectDocument).where(
            project_document_models.ProjectDocument.projectId == external_id
        )
        if not flg_deleted:
            stmt = stmt.where(project_document_models.ProjectDocument.deletedAt.is_(None))

    documents = db.execute(stmt).scalars().all()

    # Build response list
    files_list = []
    for doc in documents:
        file_info = {
            "id": doc.id,
            "fileNameOriginal": doc.fileNameOriginal,
            "contentType": doc.contentType,
            "createdAt": doc.createdAt.isoformat() if doc.createdAt else None
        }
        files_list.append(file_info)

    return files_list

@router.delete("/remove-file", response_model=Dict[str, str])
def remove_file(
    file_id: str = Query(..., alias="fileId", description="The ID of the document record (from userDocuments or projectDocuments table)."),
    prefix: str = Query(..., alias="type", description="The category or type of the file (user or project)."),
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_user_only)
) -> Dict[str, str]:
  
    if not file_id:
        raise HTTPException(status_code=400, detail="File ID cannot be empty.")

    # Validate prefix
    if prefix not in ["user", "project"]:
        raise HTTPException(status_code=400, detail=f"Unsupported prefix '{prefix}'.")

    # Find document record in database by ID
    if prefix == "user":
        stmt = select(user_document_models.UserDocument).where(
            user_document_models.UserDocument.id == file_id,
            user_document_models.UserDocument.deletedAt.is_(None)
        )
        document = db.execute(stmt).scalars().first()
    elif prefix == "project":
        stmt = select(project_document_models.ProjectDocument).where(
            project_document_models.ProjectDocument.id == file_id,
            project_document_models.ProjectDocument.deletedAt.is_(None)
        )
        document = db.execute(stmt).scalars().first()

    if not document:
        raise HTTPException(status_code=404, detail=f"File with id '{file_id}' not found in '{prefix}' documents table or already deleted.")

    # Get external_id based on document type
    external_id = document.userId if prefix == "user" else document.projectId

    # Construct file path
    file_path: Path = BASE_STORAGE_PATH / prefix / external_id / document.fileNameDisk

    # Delete file from filesystem
    try:
        if file_path.is_file():
            os.remove(file_path)
    except OSError as e:
        # Continue with DB deletion even if file deletion fails
        pass

    # Delete record from database (soft delete: set deletedAt)
    document.deletedAt = datetime.now(timezone.utc)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete record from database: {e}")

    return {"message": f"File with id '{file_id}' removed successfully."}
