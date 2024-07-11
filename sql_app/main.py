from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import crud, models, schemas
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db=db, user=user)

@app.get("/users/${user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/strategies/", response_model=schemas.Strategy)
def create_strategy_for_user(strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    try:
        db_strategy = crud.create_user_strategy(db, strategy)
        return db_strategy
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="You have already used that name.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@app.get("/strategies/{strategy_id}", response_model=schemas.Strategy)
def read_strategy(strategy_id: int, db: Session = Depends(get_db)):
    db_strategy = crud.get_strategy(db, strategy_id)
    return db_strategy

@app.get("/strategies", response_model=list[schemas.Strategy])
def read_strategies(db: Session = Depends(get_db)):
    return crud.get_strategies(db)