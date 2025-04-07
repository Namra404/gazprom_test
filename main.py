from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.api.v1.routes import device_data, user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените на ваш фронтенд-URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(device_data.router)
app.include_router(user.router)
