import httpx
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_auth_flow():
    # 1. Create Admin User
    admin_email = f"admin_{int(time.time())}@example.com"
    admin_data = {
        "email": admin_email,
        "password": "secret_admin",
        "userType": "admin",
        "roles": ["admin"],
        "nome": "Super",
        "cognome": "Admin"
    }
    
    # Note: user creation endpoint is now /users (under router, still /users prefix likely if not defined otherwise in include_router)
    # Check main.py: app.include_router(users.router) -> checks users.py: @router.post("/users") -> URL is /users
    
    print(f"Creating Admin: {admin_email}")
    response = httpx.post(f"{BASE_URL}/users", json=admin_data)
    if response.status_code != 200:
        print(f"Failed to create admin: {response.text}")
        sys.exit(1)
    
    # 2. Create Regular User
    user_email = f"user_{int(time.time())}@example.com"
    user_data = {
        "email": user_email,
        "password": "secret_user",
        "userType": "user",
        "roles": ["user"],
        "nome": "Regular",
        "cognome": "User"
    }

    print(f"Creating User: {user_email}")
    response = httpx.post(f"{BASE_URL}/users", json=user_data)
    if response.status_code != 200:
        print(f"Failed to create user: {response.text}")
        sys.exit(1)

    # 3. Login as Admin
    # Endpoint is now in auth router: @router.post("/token") -> URL is /token
    print("Logging in as Admin...")
    response = httpx.post(f"{BASE_URL}/token", data={"username": admin_email, "password": "secret_admin"})
    if response.status_code != 200:
        print(f"Admin login failed: {response.text}")
        sys.exit(1)
    admin_token = response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 4. Login as User
    print("Logging in as User...")
    response = httpx.post(f"{BASE_URL}/token", data={"username": user_email, "password": "secret_user"})
    if response.status_code != 200:
        print(f"User login failed: {response.text}")
        sys.exit(1)
    user_token = response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 5. Admin accesses Admin Endpoint
    # Url: /admin-data
    print("Test: Admin -> Admin Endpoint (Expect 200)")
    response = httpx.get(f"{BASE_URL}/admin-data", headers=admin_headers)
    if response.status_code != 200:
        print(f"FAILED: Admin/Admin access blocked: {response.status_code} {response.text}")
        sys.exit(1)
    print("PASS")

    # 6. User accesses Admin Endpoint
    print("Test: User -> Admin Endpoint (Expect 403)")
    response = httpx.get(f"{BASE_URL}/admin-data", headers=user_headers)
    if response.status_code != 403:
        print(f"FAILED: User accessed admin data! Status: {response.status_code}")
        sys.exit(1)
    print("PASS")

    # 7. User accesses User Endpoint
    # Url: /user-data
    print("Test: User -> User Endpoint (Expect 200)")
    response = httpx.get(f"{BASE_URL}/user-data", headers=user_headers)
    if response.status_code != 200:
        print(f"FAILED: User/User access blocked: {response.status_code} {response.text}")
        sys.exit(1)
    print("PASS")

    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    test_auth_flow()
