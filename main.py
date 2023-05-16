from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api import router as faq_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(faq_router, prefix="/faq")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000 , log_level="info", reload=True)