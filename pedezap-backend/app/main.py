from fastapi import FastAPI
from .routes import pedidos
from .database import Base, engine

app = FastAPI()

#Base.metadata.create_all(bind=engine)
app.include_router(pedidos.router)
