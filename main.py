from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

# Mock data
EMPLOYEES = {
    "emp001": {
        "annual": 12,
        "sick": 8,
        "latest_status": "APPROVED",
    },
    "emp002": {
        "annual": 5,
        "sick": 10,
        "latest_status": "PENDING",
    },
}

@app.get("/v1/leave")
def get_leave(employee_id: str):
    if employee_id not in EMPLOYEES:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "reason": "Employee not found"},
        )

    emp = EMPLOYEES[employee_id]
    return {
        "employee_id": employee_id,
        "annual_leave_balance": emp["annual"],
        "sick_leave_balance": emp["sick"],
        "latest_leave_status": emp["latest_status"],
        "last_updated": datetime.utcnow().isoformat() + "Z",
    }
