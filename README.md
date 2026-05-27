# Support CRM 

A fully functional customer support ticketing system built with **FastAPI + Supabase + Vanilla JS**.

## Live Demo
🔗 [Not Yet Deployed. Will Deploy soon!!]

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + FastAPI |
| Database | Supabase (PostgreSQL) |
| Frontend | HTML + CSS + Vanilla JS |
| Deployment | Railway |

## Features
- ✅ Create tickets with customer info, subject, and description
- ✅ Auto-generated ticket IDs (TKT-001, TKT-002...)
- ✅ List all tickets with clean table view
- ✅ Search across name, email, subject, description, ticket ID
- ✅ Filter by status (Open / In Progress / Closed)
- ✅ View full ticket details
- ✅ Update ticket status
- ✅ Add internal notes to tickets
- ✅ Responsive design (mobile friendly)
- ✅ Loading skeletons for better UX

## Project Structure
```
support-crm/
├── main.py           # FastAPI app entry point
├── database.py       # Supabase connection setup
├── models.py         # Database table definitions
├── schemas.py        # Request/Response validation
├── routers/
│   └── tickets.py    # All API endpoints
├── static/
│   ├── index.html    # Home — ticket list
│   ├── create.html   # Create new ticket
│   └── ticket.html   # Ticket detail & update
├── .env              # Secret keys (never committed)
├── .env.example      # Template for env variables
├── requirements.txt  # Python dependencies
└── README.md
```

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOURUSERNAME/support-crm.git
cd support-crm
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Edit `.env` and add your Supabase connection string.

### 5. Run the app
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tickets/` | Create a new ticket |
| GET | `/api/tickets/` | List all tickets (supports `?status=` and `?search=`) |
| GET | `/api/tickets/{ticket_id}` | Get full ticket details |
| PUT | `/api/tickets/{ticket_id}` | Update status or add note |
| GET | `/health` | Health check |

## Environment Variables
```
DATABASE_URL=postgresql://postgres:PASSWORD@db.REF.supabase.co:5432/postgres
```
