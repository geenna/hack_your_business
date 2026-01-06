from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import BinaryIO, Generator

class AbstractFileRepository(ABC):
    
    @abstractmethod
    def save_file(self, file: UploadFile, filename: str) -> str:
        """Salva il file e ritorna il percorso o l'ID."""
        pass

    @abstractmethod
    def get_file_path(self, filename: str) -> str:
        """Ritorna il percorso fisico del file per il download."""
        pass

    @abstractmethod
    def delete_file(self, filename: str) -> bool:
        """Cancella il file. Ritorna True se cancellato, False se non trovato."""
        pass