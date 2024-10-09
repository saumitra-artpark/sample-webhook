from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Pydantic models based on TurnIO webhook payload structure
class Profile(BaseModel):
    name: Optional[str]

class Contact(BaseModel):
    profile: Profile
    wa_id: str

class Context(BaseModel):
    from_: str = Field(..., alias='from')
    id: str

class MediaMessage(BaseModel):
    file: Optional[str]
    id: str
    link: Optional[str]
    mime_type: str
    sha256: str
    caption: Optional[str]

class LocationMessage(BaseModel):
    address: Optional[str]
    latitude: float
    longitude: float
    name: Optional[str]

class TextMessage(BaseModel):
    body: str

class SystemMessage(BaseModel):
    body: str

class Message(BaseModel):
    context: Optional[Context] = None
    from_: str = Field(..., alias='from')
    id: str
    timestamp: str
    type: str
    errors: Optional[List[Dict[str, Any]]] = None
    audio: Optional[MediaMessage] = None
    document: Optional[MediaMessage] = None
    image: Optional[MediaMessage] = None
    location: Optional[LocationMessage] = None
    system: Optional[SystemMessage] = None
    text: Optional[TextMessage] = None
    video: Optional[MediaMessage] = None
    voice: Optional[MediaMessage] = None

    class Config:
        allow_population_by_field_name = True

class WebhookPayload(BaseModel):
    contacts: List[Contact]
    messages: List[Message]
    
@app.get("/double/{number}")
async def double_number(number: int):
    """
    Endpoint that returns twice the number provided as a path parameter.
    
    :param number: The number to be doubled
    :return: A JSON object containing the result
    """
    result = number * 2
    return {"original": number, "doubled": result}


@app.post("/webhook")
async def webhook(request: Request):
    try:
        # Log the incoming request
        logger.info("Received webhook request")
        
        # Get the raw body of the request
        body = await request.json()
        logger.info(f"Webhook payload: {body}")
        
        # Parse the body into our WebhookPayload model
        payload = WebhookPayload(**body)
        
        # Process each message in the payload
        for message in payload.messages:
            await process_message(message)
        
        return {"status": "success", "message": "Webhook processed successfully"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_message(message: Message):
    """
    Process each individual message from the webhook payload.
    You can add your custom logic here to handle different types of messages.
    """
    logger.info(f"Processing message: {message}")
    
    # Example: Handle text messages
    if message.type == "text" and message.text:
        sender = message.from_
        text = message.text.body
        logger.info(f"Received text message from {sender}: {text}")
        # Add your logic here to respond to the message if needed
