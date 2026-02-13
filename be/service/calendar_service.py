from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import datetime, date
from ..persistence.model import EventoModel
from ..persistence.schemas import CalendarSchema
from . import user_service

def get_events(db: Session, start_date: date, end_date: date, calendar_types: Optional[List[str]] = None) -> List[CalendarSchema.CalendarEventResponse]:
    """
    Retrieve events within a date range, optionally filtered by calendar type.
    """
    stmt = select(EventoModel.Evento).where(
        and_(
            EventoModel.Evento.start_date >= start_date,
            EventoModel.Evento.end_date <= end_date
        )
    )

    if calendar_types:
        if isinstance(calendar_types, str):
             # If a single string is passed, interpret it as a list with one item if it's not 'all' or similar logic if needed. 
             # For now, let's assume the controller passes a list or we handle single value here.
             # The requirement says "string calendar".
             pass # Logic moved to controller or handled here if single value
        # But wait, query allows filtering by calendar type.
        # "Il rest prende i parametri ... e la stringa calendar che può essere Collaboratori,Pubblico,Personale."
        if isinstance(calendar_types, list):
             stmt = stmt.where(EventoModel.Evento.calendar.in_(calendar_types))
        else:
             stmt = stmt.where(EventoModel.Evento.calendar == calendar_types)

    events = db.execute(stmt).scalars().all()
    
    response_events = []
    for event in events:
        # Fetch guests
        guests_ids = event.guests if event.guests else []
        guests = []
        if guests_ids:
             users = user_service.get_users_by_ids(db, guests_ids)
             guests = [
                 CalendarSchema.Guest(
                     id=user.id,
                     email=user.email,
                     avatar=user.avatar,
                     name=f"{user.nome} {user.cognome}"
                 ) for user in users
             ]

        response_events.append(
            CalendarSchema.CalendarEventResponse(
                id=event.id,
                url=event.url,
                title=event.title,
                start=event.start_date,
                end=event.end_date,
                allDay=event.allDay,
                extendedProps=CalendarSchema.CalendarExtendedProps(
                    calendar=event.calendar,
                    guests=guests,
                    location=event.location,
                    description=event.description
                )
            )
        )
    
    return response_events

def create_event(db: Session, event_data: CalendarSchema.CalendarEventCreate) -> EventoModel.Evento:
    """
    Create a new event.
    """
    new_event = EventoModel.Evento(
        start_date=event_data.start,
        end_date=event_data.end,
        url=event_data.url,
        title=event_data.title,
        allDay=event_data.allDay,
        guests=event_data.extendedProps.guests,
        calendar=event_data.extendedProps.calendar,
        location=event_data.extendedProps.location,
        description=event_data.extendedProps.description
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def update_event(db: Session, event_id: str, event_data: CalendarSchema.CalendarEventUpdate) -> Optional[EventoModel.Evento]:
    """
    Update an existing event.
    """
    stmt = select(EventoModel.Evento).where(EventoModel.Evento.id == event_id)
    event = db.execute(stmt).scalars().first()

    if not event:
        return None
    
    event.start_date = event_data.start
    event.end_date = event_data.end
    event.url = event_data.url
    event.title = event_data.title
    event.allDay = event_data.allDay
    event.guests = event_data.extendedProps.guests
    event.calendar = event_data.extendedProps.calendar
    event.location = event_data.extendedProps.location
    event.description = event_data.extendedProps.description

    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: str) -> bool:
    """
    Delete an event by ID.
    """
    stmt = select(EventoModel.Evento).where(EventoModel.Evento.id == event_id)
    event = db.execute(stmt).scalars().first()

    if not event:
        return False
    
    db.delete(event)
    db.commit()
    return True
