from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="front-end")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/home/", response_class=HTMLResponse)
def load_weights(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    weight_list = crud.get_weights(db, skip=skip, limit=limit)
    return templates.TemplateResponse("home.html", {"request": request, "weight_list": weight_list})


@app.post("/home/", response_class=HTMLResponse)
def weights(request: Request, name: str = Form(...), weight: str = Form(...), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    person = schemas.WeightCreate(name=name, weight=float(weight))
    w = crud.create_user_weight(db, person)
    weight_list = crud.get_weights(db, skip=skip, limit=limit)
    return templates.TemplateResponse("home.html", {"request": request, "weight_list": weight_list})
