from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas, database # O ponto é porque estamos importando do mesmo diretório
from .database import engine, get_db

# Criação das tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Para servir arquivos estáticos (CSS, imagens, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Para renderizar templates HTML
templates = Jinja2Templates(directory="static") # Seus arquivos HTML estão dentro da pasta static

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/cadastro.html", response_class=HTMLResponse)
async def read_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.get("/login.html", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/cadastro") # Remova 'response_model=schemas.UserResponse'
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já existe"
        )

    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # --- AQUI ESTÁ A MUDANÇA PRINCIPAL ---
    # Redireciona para a página planos.html após o sucesso
    return RedirectResponse(url="/planos.html", status_code=status.HTTP_303_SEE_OTHER)

# --- Atualizando seus formulários HTML ---
@app.get("/planos.html", response_class=HTMLResponse)
async def read_planos(request: Request):
    # Aqui você renderizaria seu template planos.html
    # Se você ainda não tem planos.html, pode criar um arquivo simples dentro de 'static'
    # Ex: static/planos.html
    return templates.TemplateResponse("planos.html", {"request": request})