from sqlalchemy import Column, String, Integer, Date, ForeignKey, PrimaryKeyConstraint
from ..database import Base


class Disponibilita(Base):
    __tablename__ = "disponibilita"

    idServizio = Column(String, ForeignKey("servizi.id"))
    date = Column(Date, index=True)
    numMattina = Column(Integer)
    numPomeriggio = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint("idServizio", "date"),
    )
