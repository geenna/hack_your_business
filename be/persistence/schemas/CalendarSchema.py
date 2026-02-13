from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class Guest(BaseModel):
    id: str
    email: Optional[str] = None
    avatar: Optional[str] = None
    name: Optional[str] = None

class CalendarExtendedProps(BaseModel):
    calendar: Optional[str] = None
    guests: List[Guest] = []
    description: Optional[str] = None
    location: Optional[str] = None


class CalendarEventBase(BaseModel):
    url: Optional[str] = None
    title: str
    start: datetime 
    end: datetime 
    allDay: bool = False
    #calendar: str # [Collaboratori, Pubblico, Personale]
    invitati: Optional[List[str]] = None # List of user IDs

    class Config:
        populate_by_name = True

class CalendarEventCreate(CalendarEventBase):
    extendedProps: CalendarExtendedProps

    '''
    @model_validator(mode='before')
    @classmethod
    def extract_calendar_from_extendedProps(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'calendar' not in data and 'extendedProps' in data:
                ext_props = data['extendedProps']
                if isinstance(ext_props, dict) and 'calendar' in ext_props:
                     data['calendar'] = ext_props['calendar']
        return data
    '''

class CalendarEventUpdate(CalendarEventBase):
    extendedProps: CalendarExtendedProps

class CalendarEventResponse(BaseModel):
    id: str
    url: Optional[str] = None
    title: str
    start: datetime
    end: datetime
    allDay: bool
    extendedProps: CalendarExtendedProps

    class Config:
        from_attributes = True
