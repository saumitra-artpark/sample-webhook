SECRET="09ed2c63-a70b-4d07-ad8b-1bba548ca6fb"
PAYLOAD='{"event": "message.sent", "payload": {"message": "Test webhook", "timestamp": "2023-04-14T12:00:00Z"}}'
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')

curl -X POST https://sample-webhook-92zb.onrender.com/webhook \
     -H "Content-Type: application/json" \
     -H "X-Turn-Hook-Signature: $SIGNATURE" \
     -d "$PAYLOAD"