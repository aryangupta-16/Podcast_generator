from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models.user_model import User
from utils.auth_utils import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(data: SignupRequest):
    if User.objects(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(data.password)
    user = User(email=data.email, password=hashed_pw, name=data.name).save()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(data: LoginRequest):
    user = User.objects(email=data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id": str(user.id)}, timedelta(minutes=60))
    return {"access_token": token, "token_type": "bearer","credits": user.credits}
