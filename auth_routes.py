from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal, engine
from schemas import UserCreate, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash   
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]   
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.get("/")
async def hello():
    return {"message": "Hello, World!"}

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}

#Login endpoint
@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Auth: AuthJWT = Depends(AuthJWT), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user and check_password_hash(db_user.password, user.password):    
        # Generate tokens
        access_token = Auth.create_access_token(subject=db_user.username)
        refresh_token = Auth.create_refresh_token(subject=db_user.username)

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid credentials")
   