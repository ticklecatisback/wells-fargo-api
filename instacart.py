from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from base64 import b64encode
from typing import Any, Dict

# Initialize FastAPI app
app = FastAPI()

# Directly assigning CLIENT_ID and CLIENT_SECRET
CLIENT_ID = "Yf48pGMHj9Gj0hSPsjdGGnywg6d2A22t"
CLIENT_SECRET = "y9Ye2at5pGaxD6e0"

# Function to obtain an OAuth 2.0 token from Wells Fargo API (or similar)
def get_access_token() -> str:
    token_url = "https://api-sandbox.wellsfargo.com/oauth2/v1/token"
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = 'grant_type=client_credentials&scope=Accounts'
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")

# Pydantic model for parsing response data (customize as needed)
class ExternalApiResponse(BaseModel):
    data: Any

@app.get("/fetch-data")
async def fetch_data():
    try:
        access_token = get_access_token()
    except HTTPException as e:
        return {"error": e.detail}

    # Using a test URL for demonstration
    url = "https://httpbin.org/get"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch data from external API"}

    # Assuming the external API returns JSON data
    return {"data": response.json()}
