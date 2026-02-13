
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, date
from be.main import app
from be.api import auth
from be.persistence.model import UserModel
import uuid

# Create a test client
client = TestClient(app)

# Mock user for dependency override
mock_user = UserModel.User(
    id="test_user_id",
    email="test@example.com",
    userType="admin",
    roles=[{"action": "all", "subject": "all"}],
    nome="Test",
    cognome="User",
    user_status="ATTIVO"
)

# Function to override auth dependency
def override_allow_user():
    return mock_user

# Apply override
# Note: We need to override the specific instance of RoleChecker used in the router.
# In calendar.py: allow_user = auth.RoleChecker(["user", "admin", "CoWorking"])
# We need to find that instance or just override the dependency by matching the signature?
# FastAPI dependency overrides work by key. The key is the callable.
# Since allow_user is an instance of RoleChecker, which is callable, we need to override that specific instance.
# However, importing it from be.api.calendar might be tricky if it's not exposed or if we want to be generic.
# A strict way is to import the router's dependency.
from be.api.calendar import allow_user as calendar_allow_user

app.dependency_overrides[calendar_allow_user] = override_allow_user

def test_calendar_flow():
    print("Starting Calendar API Verification...")

    # 1. Create Event
    print("\n[1] Testing Create Event...")
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    
    event_data = {
        "title": "Test Event",
        "start_date": start_time.isoformat(),
        "end_date": end_time.isoformat(),
        "url": "http://example.com",
        "allDay": False,
        "calendar": "Collaboratori",
        "invitati": []
    }

    response = client.post("/api/calendar/crea", json=event_data)
    if response.status_code != 200:
        print(f"FAILED: {response.text}")
        return
    
    event = response.json()
    event_id = event["id"]
    print(f"SUCCESS: Created event {event_id}")
    print(f"Event: {event}")

    # 2. List Events
    print("\n[2] Testing List Events...")
    # Format dates as YYYY-MM-DD
    start_date = start_time.date().isoformat()
    end_date = (start_time + timedelta(days=1)).date().isoformat()
    
    response = client.get(f"/api/calendar/lista?start={start_date}&end={end_date}")
    if response.status_code != 200:
        print(f"FAILED: {response.text}")
        return
    
    events = response.json()
    print(f"SUCCESS: Retrieved {len(events)} events")
    found = False
    for e in events:
        if e["id"] == event_id:
            found = True
            print(f"Found created event: {e}")
            break
    
    if not found:
        print("FAILED: Created event not found in list")

    # 3. Update Event
    print("\n[3] Testing Update Event...")
    update_data = event_data.copy()
    update_data["title"] = "Updated Test Event"
    
    response = client.put(f"/api/calendar/modifica/{event_id}", json=update_data)
    if response.status_code != 200:
        print(f"FAILED: {response.text}")
        return
    
    updated_event = response.json()
    print(f"SUCCESS: Updated event")
    if updated_event["title"] != "Updated Test Event":
        print(f"FAILED: Title mismatch. Expected 'Updated Test Event', got '{updated_event['title']}'")
    else:
        print(f"verified title update: {updated_event['title']}")

    # 4. Delete Event
    print("\n[4] Testing Delete Event...")
    response = client.delete(f"/api/calendar/elimina/{event_id}")
    if response.status_code != 200:
        print(f"FAILED: {response.text}")
        return
    
    print("SUCCESS: Deleted event")

    # 5. Verify Deletion
    print("\n[5] Verifying Deletion...")
    response = client.get(f"/api/calendar/lista?start={start_date}&end={end_date}")
    events = response.json()
    found = False
    for e in events:
        if e["id"] == event_id:
            found = True
            break
    
    if found:
        print("FAILED: Event still exists after deletion")
    else:
        print("SUCCESS: Event successfully removed")

if __name__ == "__main__":
    try:
        test_calendar_flow()
    except Exception as e:
        print(f"An error occurred: {e}")
