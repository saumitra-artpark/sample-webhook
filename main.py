import os
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
import hmac
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



async def verify_signature(request: Request):
    signature = request.headers.get("X-Turn-Hook-Signature")
    if not signature:
        raise HTTPException(status_code=401, detail="No signature provided")
    
    body = await request.body()
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
    computed_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(computed_signature, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

@app.post("/webhook")
async def webhook(request: Request, verified: bool = Depends(verify_signature)):
    try:
        logger.info("Received verified webhook request")
        
        body = await request.json()
        logger.info(f"Webhook payload: {json.dumps(body, indent=2)}")
        
        # Process the webhook payload here
        # For example, check the type of event and respond accordingly
        
        with open('webhook_payload.json', 'w') as f:
            json.dump(body, f, indent=2)
        
        logger.info("Webhook payload saved to webhook_payload.json")
        return {"status": "success", "message": "Webhook processed successfully"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Keep the double number endpoint for testing purposes
@app.get("/double/{number}")
async def double_number(number: int):
    result = number * 2
    return {"original": number, "doubled": result}
