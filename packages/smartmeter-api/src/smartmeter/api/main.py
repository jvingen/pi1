from contextlib import asynccontextmanager
import asyncio
import time
from fastapi import FastAPI
from prometheus_client import make_asgi_app


app = FastAPI()

@app.get("/")
async def root():
    return {"Some": "Stuff"}

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
