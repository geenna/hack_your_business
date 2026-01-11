import sys
import os

# Add the parent directory to sys.path to allow imports
sys.path.append('/Users/geenna/work/hack_your_business')

try:
    from be.persistence.schemas import ProjectSchema
    print("ProjectSchema imported successfully")
except Exception as e:
    print(f"Error importing ProjectSchema: {e}")

try:
    from be.service import project_service
    print("project_service imported successfully")
except Exception as e:
    print(f"Error importing project_service: {e}")

try:
    from be.api import projects
    print("projects API module imported successfully")
except Exception as e:
    print(f"Error importing projects API: {e}")
