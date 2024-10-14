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
        
        # Log the raw request body
        raw_body = await request.body()
        logger.info(f"Raw request body: {raw_body}")
        
        # Check if the body is empty
        if not raw_body:
            raise ValueError("Empty request body")
        
        # Try to parse the JSON
        try:
            body = await request.json()
        except json.JSONDecodeError as json_error:
            logger.error(f"JSON parsing error: {str(json_error)}")
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(json_error)}")
        
        username = body.get("name", "Unknown User")
        id = body.get("user_id", "No ID")
        concern = body.get("message", "No concern")
        logger.info(f"Webhook payload: {json.dumps(body, indent=2)}")
        
        # Save the webhook payload to a JSON file
        # with open('webhook_payload.json', 'w') as f:
        #     json.dump(body, f, indent=2)
        
        logger.info("Webhook payload processed successfully")
        return {"status": "success", "message": f"Webhook processed successfully with\n - username: {username}\n -id: {id}\n -concern: {concern}"}
    except ValueError as ve:
        logger.error(f"Error processing webhook: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Keep the double number endpoint for testing purposes
@app.get("/double/{number}")
async def double_number(number: int):
    result = number * 2
    return {"original": number, "doubled": result}
