from fastapi import FastAPI, HTTPException

app = FastAPI(title="PPC Group HR Leave API")

# ---------------------------
# Mock Employee Leave Data
# ---------------------------
EMPLOYEE_DATA = {
    "George Mouratidis": {
        "years_of_service": 5,  # 5 years → entitlement: 22 annual
        "annual": 22 - 5,       # Approved: Feb 1-5 → 5 days used, 17 remaining
        "sick": 5 - 0,          # No approved sick in 2026 → 5 remaining
        "leave_requests": [
            {"type": "ANNUAL", "status": "APPROVED", "start": "2026-02-01", "end": "2026-02-05"},
            {"type": "ANNUAL", "status": "PENDING", "start": "2026-03-15", "end": "2026-03-20"}
        ]
    },
    "Christina Morfou": {
        "years_of_service": 8,  # 8 years → entitlement: 23 annual
        "annual": 23 - 3,       # Approved: Jan 10-12 → 3 days used, 20 remaining
        "sick": 5 - 0,          # No approved sick in 2026 → 5 remaining
        "leave_requests": [
            {"type": "ANNUAL", "status": "APPROVED", "start": "2026-01-10", "end": "2026-01-12"},
            {"type": "ANNUAL", "status": "PENDING", "start": "2026-04-01", "end": "2026-04-03"}
        ]
    },
    "Maria Papadopoulou": {
        "years_of_service": 3,  # 3 years → entitlement: 22 annual
        "annual": 22 - 0,       # No approved annual leave yet in 2026 → 22 remaining
        "sick": 5 - 1,          # Approved sick: Jan 28 → 1 day used, 3 remaining
        "leave_requests": [
            {"type": "SICK", "status": "APPROVED", "start": "2026-01-28", "end": "2026-01-26"},
            {"type": "ANNUAL", "status": "PENDING", "start": "2026-05-05", "end": "2026-05-10"}
        ]
    },
    "Dimitris Alexiou": {
        "years_of_service": 10, # 10 years → entitlement: 25 annual
        "annual": 25 - 0,       # No approved annual leave yet in 2026 → 25 remaining
        "sick": 6 - 2,          # Approved sick: Jan 15-16 → 2 days used, 4 remaining
        "leave_requests": [
            {"type": "SICK", "status": "APPROVED", "start": "2026-01-15", "end": "2026-01-16"},
            {"type": "ANNUAL", "status": "PENDING", "start": "2026-06-01", "end": "2026-06-07"}
        ]
    },
    "Eleni Papadaki": {
        "years_of_service": 2,  # 2 years → entitlement: 21 annual
        "annual": 21 - 5,       # Approved: Feb 10-14 → 5 days used, 16 remaining
        "sick": 2 - 0,          # Pending sick leave not yet approved → 2 remaining
        "leave_requests": [
            {"type": "ANNUAL", "status": "APPROVED", "start": "2026-02-10", "end": "2026-02-14"},
            {"type": "SICK", "status": "PENDING", "start": "2026-01-28", "end": "2026-01-28"}
        ]
    }
}


# ---------------------------
# API Endpoint
# ---------------------------
@app.get("/v1/leave")
def get_leave(employee_id: str):
    """
    Returns leave balances, years of service, and detailed leave request info for a given employee.
    """
    name = employee_id.strip()
    if name not in EMPLOYEE_DATA:
        raise HTTPException(status_code=400, detail=f"Employee '{name}' not found")

    emp = EMPLOYEE_DATA[name]

    return {
        "employee_id": name,
        "years_of_service": emp["years_of_service"],
        "annual_leave_balance": emp["annual"],
        "sick_leave_balance": emp["sick"],
        "leave_requests": emp["leave_requests"],
        "currently_on_leave": None,  # not computed without datetime
    }
