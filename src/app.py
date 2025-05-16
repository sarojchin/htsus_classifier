from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductRequest(BaseModel):
    description: str

@app.post("/classify")
async def classify_product(req: ProductRequest):
    desc = req.description.lower()
    if "steel" in desc:
        code = "7323.93.0060"
    elif "plastic" in desc:
        code = "3926.90.9990"
    else:
        code = "0000.00.0000"
    return {"classification_code": code}
