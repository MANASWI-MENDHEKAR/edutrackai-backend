# from fastapi import FastAPI, UploadFile, File, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session
# from dotenv import load_dotenv
# import os
# from pydantic import BaseModel
# from typing import List
# from fastapi.responses import JSONResponse
# from fastapi import FastAPI, HTTPException
# import psycopg2


# # Load environment variables from .env file
# load_dotenv()

# # Example usage
# db_url = os.getenv("DATABASE_URL")
# minio_key = os.getenv("MINIO_ACCESS_KEY")


# # Import model and base
# from models import Base, Performance

# app = FastAPI()

# # CORS setup
# origins = [
#     "http://localhost:5173"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# #  SQLite setup
# DATABASE_URL = "sqlite:///./dev.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# #  Create tables
# Base.metadata.create_all(bind=engine)

# # Dependency for DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# #  In-memory cache (replaces Redis)
# cache = {}

# #  Local file storage (replaces MinIO)
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# #  Health check
# @app.get("/api/health")
# def health_check():
#     return {"status": "ok", "message": "API is running"}

# #  File upload
# @app.post("/api/upload")
# async def upload_file(file: UploadFile = File(...)):
#     file_location = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_location, "wb") as f:
#         f.write(await file.read())
#     return {"filename": file.filename, "message": "File saved locally"}

# #  Cache endpoints
# @app.get("/api/cache/{key}")
# def get_cache(key: str):
#     value = cache.get(key)
#     return {"key": key, "value": value}

# @app.post("/api/cache/{key}")
# def set_cache(key: str, value: str):
#     cache[key] = value
#     return {"message": f"Stored {key} = {value}"}

# #  Insert performance record
# @app.post("/api/performance")
# def create_performance(institution: str, metric: str, value: int, db: Session = Depends(get_db)):
#     record = Performance(institution=institution, metric=metric, value=value)
#     db.add(record)
#     db.commit()
#     db.refresh(record)
#     return {"message": "Record added", "id": record.id}

# @app.get("/api/performance")
# def list_performance(db: Session = Depends(get_db)):
#     records = db.query(Performance).all()
#     return [
#         {
#             "id": r.id,
#             "institution": r.institution,
#             "metric": r.metric,
#             "value": r.value
#         }
#         for r in records
#     ]

# class UserPerformance(BaseModel):
#     user_id: str
#     name: str
#     score: int
#     remarks: str

# from typing import List

# class UserPerformance(BaseModel):
#     user_id: int
#     name: str
#     score: int
#     remarks: str

# @app.get("/userPerformance/GetUserPerformance", response_model=List[UserPerformance])
# def get_user_performance():
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             port="5432",
#             user="postgres",
#             password="Sih@123456",  # replace with your actual password
#             database="sihdb"
#         )
#         cur = conn.cursor()
#         cur.execute("SELECT user_id, name, score, remarks FROM public.user_performance ORDER BY user_id ASC;")
#         rows = cur.fetchall()
#         cur.close()
#         conn.close()

#         # Convert rows to list of dicts
#         result = [
#             {"user_id": r[0], "name": r[1], "score": r[2], "remarks": r[3]}
#             for r in rows
#         ]
#         return result

#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail=str(e))


# from dotenv import load_dotenv
# load_dotenv()

# conn = psycopg2.connect(
#     host=os.getenv("DB_HOST"),
#     port=os.getenv("DB_PORT"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASS"),
#     database=os.getenv("DB_NAME")
# )

# from pydantic import BaseModel

# class UserPerformance(BaseModel):
#     id: int
#     score: int
#     remarks: str












from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import os
import psycopg2

# Load environment variables
load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv("DB_URL", "sqlite:///./dev.db")

# SQLAlchemy setup
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Import model
from models import Performance

# FastAPI app
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In-memory cache
cache = {}

# Local file storage
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Health check
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

# File upload
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "message": "File saved locally"}

# Cache endpoints
@app.get("/api/cache/{key}")
def get_cache(key: str):
    value = cache.get(key)
    return {"key": key, "value": value}

@app.post("/api/cache/{key}")
def set_cache(key: str, value: str):
    cache[key] = value
    return {"message": f"Stored {key} = {value}"}

# Insert performance record
@app.post("/api/performance")
def create_performance(institution: str, metric: str, value: int, db: Session = Depends(get_db)):
    record = Performance(institution=institution, metric=metric, value=value)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": "Record added", "id": record.id}

@app.get("/api/performance")
def list_performance(db: Session = Depends(get_db)):
    records = db.query(Performance).all()
    return [
        {
            "id": r.id,
            "institution": r.institution,
            "metric": r.metric,
            "value": r.value
        }
        for r in records
    ]

# Pydantic model for user performance
class UserPerformance(BaseModel):
    user_id: int
    name: str
    score: int
    remarks: str

# Get user performance
@app.get("/userPerformance/GetUserPerformance", response_model=List[UserPerformance])
def get_user_performance():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cur = conn.cursor()
        cur.execute("SELECT user_id, name, score, remarks FROM public.user_performance ORDER BY user_id ASC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {"user_id": r[0], "name": r[1], "score": r[2], "remarks": r[3]}
            for r in rows
        ]
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))

# Test DB connection
@app.get("/test-db")
def test_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        conn.close()
        return {"status": "success", "message": "Connected to PostgreSQL"}
    except Exception as e:
        print("DB connection error:", e)
        return {"status": "error", "message": str(e)}

# Create user_performance table
@app.get("/init-user-performance-table")
def init_user_performance_table():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.user_performance (
                user_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                score INTEGER,
                remarks TEXT
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Table created or already exists"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.get("/")
def root():
    return {"message": "Welcome to EduTrackAI Backend. Visit /docs for API documentation."}

import requests

@app.post("/api/upload-to-minio")
async def upload_to_minio(file: UploadFile = File(...)):
    endpoint = os.getenv("MINIO_ENDPOINT")  # e.g. "your-minio-host:9000"
    bucket = os.getenv("MINIO_BUCKET_NAME")  # e.g. "uploads"
    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")

    content = await file.read()
    url = f"http://{endpoint}/{bucket}/{file.filename}"

    response = requests.put(
        url,
        data=content,
        headers={"Content-Type": file.content_type},
        auth=(access_key, secret_key)
    )

    if response.status_code in [200, 204]:
        return {"message": "File uploaded to MinIO", "filename": file.filename}
    else:
        return {"error": response.text, "status_code": response.status_code}