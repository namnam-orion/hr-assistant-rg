import logging
from fastapi import FastAPI
from .routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

app = FastAPI(title="HR Policy Assistant")
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logging.info("HR Policy Assistant API started.")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("HR Policy Assistant API shutting down.")
