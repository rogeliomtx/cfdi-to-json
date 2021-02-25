from fastapi import File, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from handlers import CFDIHandler

# uvicorn main:app --reload
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("cfdis/supported_versions/")
async def get_supported_versions():
    return {"cfdi": ["3.3"], "nomina": ["1.2"]}


@app.post("/cfdis/files/")
async def read_cfdi(file: UploadFile = File(...)):
    data = CFDIHandler.to_json(file)
    return data
