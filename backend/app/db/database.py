import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
# 1. The Database Connection URL
# We use +psycopg2 to specify the driver, and ?sslmode=require for Neon's secure connection
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASe_URL")

# 2. Create the Engine
# The engine is the core interface to the database. It manages the connection pool.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True # <--- Crucial for serverless DBs like Neon!
)

# 3. Create the Session Factory
# This creates a blueprint for making database sessions. 
# autocommit=False: We manually control when to save (commit) data.
# autoflush=False: We manually control when to send pending changes to the DB.
# bind=engine: Tells the session to use the engine we just created.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Dependency (The "Bridge" to your API routes)
def get_db():
    # Create a new session for this specific API request
    db = SessionLocal()
    try:
        # 'yield' pauses here and gives the 'db' session to your API route.
        # The route does its work (queries, inserts, etc.).
        yield db
    finally:
        # Once the API route is completely finished (success or error), 
        # this code runs to close the connection and return it to the pool.
        db.close()