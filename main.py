from fastapi import FastAPI, Request, HTTPException
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Log the incoming request
        logger.info("Received webhook request")
        
        # Get the raw body of the request
        body = await request.json()
        
        # Log the entire webhook payload as JSON
        logger.info(f"Webhook payload: {json.dumps(body, indent=2)}")
        
        # Save the webhook payload to a JSON file
        with open('webhook_payload.json', 'w') as f:
            json.dump(body, f, indent=2)
        
        logger.info("Webhook payload saved to webhook_payload.json")
        return {"status": "success", "message": "Webhook payload logged successfully"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Keep the double number endpoint for testing purposes
@app.get("/double/{number}")
async def double_number(number: int):
    result = number * 2
    return {"original": number, "doubled": result}
