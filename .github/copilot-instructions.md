# AI Coding Agent Instructions for Hack Your Business

## Project Overview
Full-stack business management application with Italian localization. Backend: FastAPI + SQLAlchemy (SQLite). Frontend: Vue 3 + Vuetify 3 + TypeScript + Pinia.

## Architecture
- **Backend Structure**: `be/` contains FastAPI app with modular design:
  - `api/`: Route handlers (auth, users, payments, projects, repository)
  - `persistence/`: Database models (`model/`), schemas (`schemas/`), database config
  - `service/`: Business logic layer (e.g., `project_service.py` for project operations)
  - `main.py`: App initialization, CORS for `localhost:5173`, table creation
- **Frontend Structure**: `fe/src/` with `@core/` utilities, `@layouts/`, auto-imported components/plugins
- **Data Flow**: API endpoints call services → services query models → return Pydantic schemas
- **File Storage**: Local directories `repository/project/{uuid}/`, `repository/user/{uuid}/` for uploads

## Key Patterns & Conventions

### Backend
- **Database Queries**: Use SQLAlchemy 2.0 `select()` syntax, e.g.:
  ```python
  stmt = select(UserModel.User).where(UserModel.User.email == email)
  user = db.execute(stmt).scalars().first()
  ```
- **Models**: UUID primary keys as strings, JSON columns for complex data (e.g., `roles` as `List[dict]` with `action`/`subject`)
- **Auth**: JWT tokens with CASL ability rules returned in login response
- **Migrations**: Manual SQLite ALTER TABLE scripts (e.g., `add_user_status_column.py`)
- **Seeding**: Direct SQLite connections in scripts like `seed_payments.py` for test data

### Frontend
- **State Management**: Pinia stores in `src/stores/`, auto-imported
- **Routing**: Vue Router auto-generated from `src/pages/`, kebab-case route names
- **Components**: Auto-imported via `unplugin-vue-components`, Vuetify components available globally
- **Plugins**: Auto-registered from `src/plugins/` directory
- **Styling**: SCSS with Vuetify variables in `src/assets/styles/variables/_vuetify.scss`
- **Abilities**: CASL integration for role-based UI (rules from backend login)

## Developer Workflows

### Running the Application
- **Backend**: `cd be && uvicorn main:app --reload` (docs at `/api/docs`)
- **Frontend**: `cd fe && npm run dev` (serves on `localhost:5173`)
- **Database**: SQLite file `sql_app.db` in root, echo=True for query logging

### Building & Deployment
- **Frontend Build**: `cd fe && npm run build` (outputs to `dist/`)
- **Type Checking**: `cd fe && npm run type-check` (vue-tsc)
- **Linting**: `cd fe && npm run lint` (ESLint with Vue/Airbnb rules)
- **Clean**: `cd fe && npm run clean` (removes generated JS files)

### Database Operations
- **Verify/Seed**: Run `python verify_db.py` or `python seed_payments.py` from root
- **Migrations**: Execute scripts like `python add_telefono_column.py` for schema changes
- **Reset**: Delete `sql_app.db` and re-run `python be/main.py` to recreate tables

### File Uploads
- **Project Files**: Store in `repository/project/{project_uuid}/`
- **User Files**: Store in `repository/user/{uuid}/`
- **API**: Use `repository.py` endpoints for file operations

## Common Tasks
- **Add API Endpoint**: Create router in `be/api/`, include in `main.py` api_router
- **Add Model Field**: Update model in `persistence/model/`, create migration script, update schema
- **Add Frontend Page**: Create `.vue` in `src/pages/`, auto-routes via VueRouter plugin
- **Add Component**: Place in `src/components/`, auto-imported (no manual import needed)
- **Update Abilities**: Modify user `roles` JSON, use `@casl/vue` directives in templates

## Dependencies
- **Backend**: FastAPI, SQLAlchemy, Pydantic, python-jose for JWT
- **Frontend**: Vue 3, Vuetify 3, Pinia, Vue Router, Axios for API calls
- **Dev Tools**: ESLint, vue-tsc, Vite with hot reload

Reference: `be/main.py`, `fe/package.json`, `be/persistence/model/UserModel.py` for examples.</content>
<parameter name="filePath">/Users/geenna/work/hack_your_business/.github/copilot-instructions.md