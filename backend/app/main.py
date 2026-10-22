from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db, engine
from sqlalchemy import text

app = FastAPI(title="Job Fair API")

# Optional: A simple health check route to prove the DB is connected
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Execute a simple, raw SQL command to test the connection
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Database is connected!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Fair API"}