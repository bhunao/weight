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


@app.get("/", response_class=HTMLResponse)
def home(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    weight_list = crud.get_weights(db, skip=skip, limit=limit)
    return templates.TemplateResponse("home.html", {"request": request, "weight_list": weight_list})


@app.post("/", response_class=HTMLResponse)
def home(request: Request, name: str = Form(...), weight: str = Form(...), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    person = schemas.WeightCreate(name=name, weight=float(weight))
    crud.create_user_weight(db, person)
    weight_list = crud.get_weights(db, skip=skip, limit=limit)
    return templates.TemplateResponse("home.html", {"request": request, "weight_list": weight_list})


@app.post("/", response_class=HTMLResponse)
def search(request: Request, name_search: str = Form(...), db: Session = Depends(get_db)):
    weight_list = crud.get_weight_by_name(db, name_search)
    return templates.TemplateResponse("weight.html", {"request": request, "weight_list": weight_list, "name": name_search})


@app.get('/w', response_class=HTMLResponse)
def weight(request: Request, name: str, db: Session = Depends(get_db)):
    weight_list = crud.get_weight_by_name(db, name)
    return templates.TemplateResponse("weight.html", {"request": request, "weight_list": weight_list, "name": name})


@app.get('/test')
def test(name_search: str):
    print(f'test worked {name_search=}')
    return name_search