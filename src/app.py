from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
import json
from sqlalchemy.orm import Session
from src.database import get_db, Classification

app = FastAPI()

# Allow React frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://htsus-classifier-a7n98nc5j-sarojchins-projects.vercel.app/"],  # React dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductRequest(BaseModel):
    description: str



# Initialize Bedrock client
brt = boto3.client("bedrock-runtime", region_name="us-west-2",
                    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
                    )
model_id = "amazon.titan-text-express-v1"

def classify_with_bedrock(description: str) -> str:
    user_message = f"""You are a professional customs broker with complete knowledge of the HTSUS, general rules of interpretation, and all relevant rulings. Given a product and its description, you are able to return the exact classification code and tariff rate in the format:
Product: [Product Name]  
HTSUS Code: [Code]  
Tariff Rate: [Rate]  
The product is {description}. 
"""     

    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        response = brt.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0, "topP": 0},
        )
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text.strip()    
    except Exception as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return "ERROR: Failed to classify product."




@app.post("/classify")
async def classify_product(req: ProductRequest, db: Session = Depends(get_db)):
    print("Product description: ", req.description)
    classification_response = classify_with_bedrock(req.description)
    print("Classification response: ", classification_response)
    
    db_classification = Classification(
        product_description=req.description,
        classification_result=classification_response
    )
    db.add(db_classification)
    db.commit()
    db.refresh(db_classification)
    
    return {"classification": classification_response}  



@app.get("/test")
async def test_endpoint(db: Session = Depends(get_db)):
    db_classification = Classification(
        product_description="SAMPLE",
        classification_result="SAMPLE_RESULT"
    )
    db.add(db_classification)
    db.commit()
    db.refresh(db_classification)
    return {"message": "API is working!"}

