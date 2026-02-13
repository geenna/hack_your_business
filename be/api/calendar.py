from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..persistence.schemas import CalendarSchema
from ..persistence.model import EventoModel, UserModel
from ..service import calendar_service
from .. import auth

router = APIRouter(
    prefix="/calendar",
    tags=["calendar"]
)

# Reuse auth dependencies or create new ones if needed
# For now, I'll assume users need to be authenticated to access calendar
allow_user = auth.RoleChecker(["user", "all", "CoWorking"]) # Adjust roles as per requirements

@router.get("/lista", response_model=List[CalendarSchema.CalendarEventResponse])
def list_events(
    start: date,
    end: date,
    calendar: Optional[str] = Query(None, description="Calendar type (Collaboratori, Pubblico, Personale)"),
    db: Session = Depends(auth.get_db),
    current_user: UserModel.User = Depends(allow_user)
):
    """
    Get a list of events filtered by date range and optional calendar type.
    """
    events = calendar_service.get_events(db, start, end, calendar)
    return events

@router.post("/crea", response_model=CalendarSchema.CalendarEventResponse) # Note: Response model might need adjustment as service returns DB model, but we want enriched response?
# Actually, for create, usually we return what was created. 
# The service create_event returns EventoModel.Evento.
# The schema CalendarEventResponse expects 'extendedProps'.
# Implementation detail: create_event in service returns the DB object.
# We should probably return the created object. However, the client might expect the same format.
# Let's adjust the return to simple ID or the created object mapping.
# For simplicity, let's return the created object and let Pydantic handle it, 
# BUT EventoModel doesn't have extendedProps directly.
# We should probably re-fetch or construct the response. 
# Let's construct it manually or fetch it.
def create_event(
    event_data: CalendarSchema.CalendarEventCreate,
    db: Session = Depends(auth.get_db),
    current_user: UserModel.User = Depends(allow_user)
):
    """
    Create a new calendar event.
    """
    new_event = calendar_service.create_event(db, event_data)
    
    # Construct response with empty guests for now, or fetch them if needed
    # Since we just created it, we know the guests IDs.
    # Let's reuse the get logic or just return basic. 
    # The requirement didn't specify return type for create, but consistency is good.
    # Let's try to return the full response.
    
    # We can use the service to get the single event or just mock the extended props
    # Since we have guests IDs in event_data, we can use user_service again.
    from ..service import user_service
    guests = []
    if new_event.guests:
        users = user_service.get_users_by_ids(db, new_event.guests)
        guests = [
                 CalendarSchema.Guest(
                     id=user.id,
                     email=user.email,
                     avatar=user.avatar,
                     name=f"{user.nome} {user.cognome}"
                 ) for user in users
             ]

    return CalendarSchema.CalendarEventResponse(
        id=new_event.id,
        url=new_event.url,
        title=new_event.title,
        start=new_event.start_date,
        end=new_event.end_date,
        allDay=new_event.allDay,
        extendedProps=CalendarSchema.CalendarExtendedProps(
            calendar=new_event.calendar,
            guests=guests,
            location=new_event.location,
            description=new_event.description
        )
    )

@router.put("/modifica/{event_id}", response_model=CalendarSchema.CalendarEventResponse)
def update_event(
    event_id: str,
    event_data: CalendarSchema.CalendarEventUpdate,
    db: Session = Depends(auth.get_db),
    current_user: UserModel.User = Depends(allow_user)
):
    """
    Update an existing calendar event.
    """
    updated_event = calendar_service.update_event(db, event_id, event_data)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Construct response
    from ..service import user_service
    guests = []
    if updated_event.guests:
         users = user_service.get_users_by_ids(db, updated_event.guests)
         guests = [
                 user.id for user in users
             ]

    return CalendarSchema.CalendarEventResponse(
        id=updated_event.id,
        url=updated_event.url,
        title=updated_event.title,
        start=updated_event.start_date,
        end=updated_event.end_date,
        allDay=updated_event.allDay,
        extendedProps=CalendarSchema.CalendarExtendedProps(
            calendar=updated_event.calendar,
            guests=guests,
            location=updated_event.location,
            description=updated_event.description
        )
    )

@router.delete("/elimina/{event_id}")
def delete_event(
    event_id: str,
    db: Session = Depends(auth.get_db),
    current_user: UserModel.User = Depends(allow_user)
):
    """
    Delete a calendar event.
    """
    success = calendar_service.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {"message": "Event deleted successfully"}
