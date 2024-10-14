import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import json

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

@app.post("/webhook")
async def webhook(request: Request):
    try:
        logger.info("Received webhook request")
        
        body = await request.json()
        logger.info(f"Webhook payload: {json.dumps(body, indent=2)}")
        
        # Save the webhook payload to a JSON file
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
