import os
import requests
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_variable(key: str) -> str:
    """Get environment variable from .env file"""
    # Convert the key format to environment variable format
    env_key = key.replace('f/secrets/', '').replace('/', '_').upper()
    value = os.getenv(env_key)
    
    if not value:
        raise ValueError(f"Environment variable {env_key} not found. Please check your .env file.")
    
    return value

def get_connection_credentials(id: str, providerConfigKey: str) -> Dict[str, Any]:
    """Get credentials from Nango"""
    base_url = get_variable("f/secrets/nango/nango_base_url")
    secret_key = get_variable("f/secrets/nango/nango_secret_key")
    
    url = f"{base_url}/connection/{id}"
    params = {
        "provider_config_key": providerConfigKey,
        "refresh_token": "true",
    }
    headers = {"Authorization": f"Bearer {secret_key}"}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise exception for bad status codes
    
    return response.json()

def create_credentials_from_nango(nango_response: Dict[str, Any]) -> Credentials:
    """Create Google credentials object from Nango response"""
    
    # Extract token information from Nango response
    # Adjust these keys based on your actual Nango response structure
    credentials_data = nango_response.get('credentials', nango_response)
    
    # Common fields that might be in Nango response
    access_token = credentials_data.get('access_token')
    refresh_token = credentials_data.get('refresh_token')
    token_uri = 'https://oauth2.googleapis.com/token'
    client_id = credentials_data.get('client_id')
    client_secret = credentials_data.get('client_secret')
    
    if not access_token:
        raise ValueError("No access_token found in Nango response")
    
    # Create OAuth2 credentials object
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=token_uri,
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES
    )
    
    return creds

def authenticate_gmail_with_nango(connection_id: str, provider_config_key: str = "google") -> build:
    """Authenticate Gmail using Nango and return Gmail service object"""
    
    try:
        # Get credentials from Nango
        print(f"Getting credentials for connection: {connection_id}")
        nango_response = get_connection_credentials(connection_id, provider_config_key)
        
        # Create Google credentials from Nango response
        creds = create_credentials_from_nango(nango_response)
        
        # Refresh token if needed
        if not creds.valid and creds.refresh_token:
            print("Refreshing access token...")
            creds.refresh(Request())
        
        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)
        print("Gmail API authenticated successfully with Nango!")
        
        return service
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Nango: {e}")
        raise
    except Exception as e:
        print(f"Error authenticating with Gmail: {e}")
        raise

# Alternative version if Nango response structure is different
def authenticate_gmail_with_nango_v2(connection_id: str, provider_config_key: str = "google") -> build:
    """Alternative version - adjust based on your Nango response structure"""
    
    try:
        # Get credentials from Nango
        nango_response = get_connection_credentials(connection_id, provider_config_key)
        
        # Debug: Print response structure (remove in production)
        print("Nango response structure:", list(nango_response.keys()))
        
        # Try different response structures
        access_token = None
        refresh_token = None
        
        # Check multiple possible locations for tokens
        if 'access_token' in nango_response:
            access_token = nango_response['access_token']
            refresh_token = nango_response.get('refresh_token')
        elif 'credentials' in nango_response:
            creds_data = nango_response['credentials']
            access_token = creds_data.get('access_token')
            refresh_token = creds_data.get('refresh_token')
        elif 'token' in nango_response:
            access_token = nango_response['token']
            refresh_token = nango_response.get('refresh_token')
        
        if not access_token:
            raise ValueError(f"No access token found in Nango response. Available keys: {list(nango_response.keys())}")
        
        print(f"Found access token: {access_token[:20]}...")
        
        # Create OAuth2 credentials
        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=None,  # Not required for existing tokens
            client_secret=None,  # Not required for existing tokens
            scopes=SCOPES
        )
        
        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)
        print("Gmail API authenticated successfully with Nango!")
        
        return service
        
    except Exception as e:
        print(f"Error in authentication: {e}")
        print("Full Nango response for debugging:")
        try:
            nango_response = get_connection_credentials(connection_id, provider_config_key)
            print(nango_response)
        except:
            print("Could not fetch Nango response for debugging")
        raise

