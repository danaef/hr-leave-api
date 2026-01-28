from fastapi import FastAPI, HTTPException
from datetime import date, datetime

app = FastAPI(title="PPC Group HR Leave API")

# ---------------------------
# Mock Employee Leave Data
# ---------------------------
EMPLOYEE_DATA = {
    "Grigoris Katsaros": {
        "annual": 10,
        "sick": 5,
        "leave_requests": [
            {"type": "ANNUAL", "status": "APPROVED", "start": "2026-02-01", "end": "2026-02-05"},
            {"type": "SICK", "status": "APPROVED", "start": "2025-12-10", "end": "2025-12-12"},
            {"type": "ANNUAL", "status": "PENDING", "start": "2026-03-15", "end": "2026-03-20"}
        ]
    },
    "Iordanis Paraskevas": {
        "annual": 15,
        "sick": 3,
        "leave_requests": [
            {"type": "ANNUAL", "status": "APPROVED", "start": "2026-01-10", "end": "2026-01-12"},
            {"type": "SICK", "status": "APPROVED", "start": "2025-11-05", "end": "2025-11-06"},
            {"type": "ANNUAL", "status": "PENDING", "start": "2026-04-01", "end": "2026-04-03"}
        ]
    },
    "Maria Papadopoulou": {
        "annual": 12,
        "sick": 4,
        "leave_requests": [
            {"type": "SICK", "status": "APPROVED", "start": str(date.today()), "end": str(date.today())},
            {"type": "ANNUAL", "status": "APPROVED", "start": "2025-12-20", "end": "2025-12-25"},
            {"type": "ANNUAL", "status": "PENDING", "start": "2026-05-05", "end": "2026-05-10"}
        ]
    },
    "Dimitris Alexiou": {
        "annual": 8,
        "sick": 6,
        "leave_requests": [
            {"type": "SICK", "status": "APPROVED", "start": "2026-01-15", "end": "2026-01-16"},
            {"type": "ANNUAL", "status": "APPROVED", "start": "2025-10-05", "end": "2025-10-10"},
            {"type": "ANNUAL", "status": "PENDING", "start": "2026-06-01", "end": "2026-06-07"}
        ]
    },
    "Eleni Papadaki": {
        "annual": 20,
        "sick": 2,
        "leave_requests": [
            {"type": "ANNUAL", "status": "APPROVED", "start": "2026-02-10", "end": "2026-02-15"},
            {"type": "SICK", "status": "PENDING", "start": "2026-01-28", "end": "2026-01-28"},
            {"type": "ANNUAL", "status": "APPROVED", "start": "2025-08-01", "end": "2025-08-05"}
        ]
    }
}

# ---------------------------
# API Endpoint
# ---------------------------
@app.get("/v1/leave")
def get_leave(employee_id: str):
    """
    Returns leave balances and detailed leave request info for a given employee.
    """
    name = employee_id.strip()
    if name not in EMPLOYEE_DATA:
        raise HTTPException(status_code=400, detail=f"Employee '{name}' not found")

    emp = EMPLOYEE_DATA[name]

    # Determine if employee is currently on leave today
    today = date.today()
    current_leave = None
    for req in emp["leave_requests"]:
        start = datetime.strptime(req["start"], "%Y-%m-%d").date()
        end = datetime.strptime(req["end"], "%Y-%m-%d").date()
        if start <= today <= end and req["status"] == "APPROVED":
            current_leave = req
            break

    return {
        "employee_id": name,
        "annual_leave_balance": emp["annual"],
        "sick_leave_balance": emp["sick"],
        "leave_requests": emp["leave_requests"],
        "currently_on_leave": current_leave if current_leave else None,
        "last_updated": datetime.utcnow().isoformat() + "Z",
    }
