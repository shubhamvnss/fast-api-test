
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr
import sqlite3
import logging
from typing import List

# ---------- Logging Setup ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()


# ---------- Pydantic Schema ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6)

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr


# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

init_db()



@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (user.name, user.email, user.password)
        )
        conn.commit()
        conn.close()
        logging.info(f"User created: {user.email}")
        return {"message": "User created successfully!"}
    except sqlite3.IntegrityError:
        logging.warning(f"User with email already exists: {user.email}")
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        logging.exception("Unexpected error while creating user.")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/users/", response_model=List[UserRead])
def get_users():
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        conn.close()
        logging.info("Fetched users list.")
        return [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
    except Exception as e:
        logging.exception("Error fetching users.")
        raise HTTPException(status_code=500, detail="Failed to fetch users.")


