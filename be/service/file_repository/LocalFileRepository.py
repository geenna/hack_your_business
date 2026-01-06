import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from .AbstractFileRepository import AbstractFileRepository

class LocalFileRepository(AbstractFileRepository):
    def __init__(self, upload_dir: str = "uploads"):
        # Crea la cartella se non esiste
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def set_upload_dir(self, upload_dir: str =  "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        

    def save_file(self, file: UploadFile, filename: str) -> str:
        destination = self.upload_dir / filename
        
        try:
            with destination.open("wb") as buffer:
                # Copia lo stream del file nel file di destinazione
                shutil.copyfileobj(file.file, buffer)
            return str(destination)
        finally:
            file.file.close()

    def get_file_path(self, filename: str) -> str:
        path = self.upload_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"File {filename} non trovato.")
        return str(path)

    def delete_file(self, filename: str) -> bool:
        path = self.upload_dir / filename
        if path.exists():
            os.remove(path)
            return True
        return False