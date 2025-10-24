# EduTrackAI Backend – User Performance Module

This FastAPI backend provides endpoints to retrieve user performance data from a PostgreSQL database. It supports local and containerized deployment, and is demo-ready for SIH judging.

---

## Setup Instructions

### 1. Clone the Repo & Enter Backend Folder

```bash
git clone <your-repo-url>
cd backend

### 2. Create Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## 3. Install Dependencies

pip install -r requirements.txt

## 4. Configure .env

Create a .env file with the following:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sihdb
DB_USER=postgres
DB_PASS=Sih@123456

MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

## 5. Run the Server
uvicorn main:app --reload



### API Documentation

Visit Swagger UI:
http://localhost:8000/docs


## You’ll see all available endpoints with example responses.

# Sample Endpoint
# Get User Performance

curl -X GET http://localhost:8000/userPerformance/GetUserPerformance

[
  {
    "user_id": 1,
    "name": "John",
    "score": 85,
    "remarks": "Excellent"
  }
]






