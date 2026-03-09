import requests

def send_webhook_alert(webhook_url, message):
    payload = {
        "text": message
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
       
       if response.status_code == 200:
            return{
                "status": "SENT"
            }
        return{
            "status": "FAILED",
            "error": response.text
        }
    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e)
        }