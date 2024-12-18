from fastapi import FastAPI
import uvicorn
from config.prsma_config import connect_prisma, disconnect_prisma
from routers.user_router import router as user_router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await connect_prisma()


@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_prisma()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# routers
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
