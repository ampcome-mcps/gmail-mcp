# Gmail API with Nango - Complete Setup Guide

## Step 1: Project Setup

### Create project directory
```bash
mkdir gmail-nango-project
cd gmail-nango-project
```

### Create virtual environment (recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Step 2: Install Dependencies

### Install required packages
```bash
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 python-dotenv requests
```

### Create requirements.txt
```bash
pip freeze > requirements.txt
```

## Step 3: Create Project Files

### 1. Create `.env` file
Create a file named `.env` in your project root:

```bash
# Create .env file
touch .env  # On Windows: type nul > .env
```

Add this content to `.env`:
```
# Nango Configuration
NANGO_NANGO_BASE_URL=https://api.nango.dev
NANGO_NANGO_SECRET_KEY=your-actual-nango-secret-key

# Gmail Connection
GMAIL_CONNECTION_ID=your-actual-connection-id
NANGO_PROVIDER_CONFIG_KEY=google
```

### 2. Create the main Python file
Create `gmail_client.py` and copy the Gmail authentication code into it.

### 3. Create .gitignore
```bash
# Create .gitignore
touch .gitignore  # On Windows: type nul > .gitignore
```

Add this content:
```
# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

## Step 4: Get Your Nango Credentials

### From your Nango dashboard:
1. **Base URL**: Usually `https://api.nango.dev` or your self-hosted URL
2. **Secret Key**: Found in your Nango project settings
3. **Connection ID**: The ID of the user's Gmail connection in Nango
4. **Provider Config Key**: The key you set up for Google in Nango (usually 'google')

### Update your `.env` file with real values:
```
NANGO_NANGO_BASE_URL=https://api.nango.dev
NANGO_NANGO_SECRET_KEY=sk_your_actual_secret_key_here
GMAIL_CONNECTION_ID=user_123_gmail_connection
NANGO_PROVIDER_CONFIG_KEY=google
```

## Step 5: Test the Setup

### Simple test script
Create `test_connection.py`:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_variables():
    """Test if all required environment variables are set"""
    required_vars = [
        'NANGO_NANGO_BASE_URL',
        'NANGO_NANGO_SECRET_KEY', 
        'GMAIL_CONNECTION_ID',
        'NANGO_PROVIDER_CONFIG_KEY'
    ]
    
    print("Testing environment variables...")
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {'*' * len(value)}")  # Mask the value
        else:
            print(f"✗ {var}: Not found!")
            all_good = False
    
    return all_good

if __name__ == '__main__':
    if test_env_variables():
        print("\n✓ All environment variables are set!")
        print("Ready to run the Gmail client.")
    else:
        print("\n✗ Please check your .env file.")
```

Run the test:
```bash
python test_connection.py
```

## Step 6: Run the Gmail Client

### Run the main script
```bash
python gmail_client.py
```

### Expected output if successful:
```
Getting credentials for connection: user_123_gmail_connection
Gmail API authenticated successfully with Nango!
Connected to Gmail for: user@example.com
Ready to use Gmail API!
Found 5 recent messages
```

### Common error messages and solutions:

**Error: "Environment variable NANGO_NANGO_BASE_URL not found"**
- Solution: Check your `.env` file exists and has the correct variable names

**Error: "Error connecting to Nango: 401 Unauthorized"**
- Solution: Check your `NANGO_NANGO_SECRET_KEY` is correct

**Error: "Error connecting to Nango: 404 Not Found"**
- Solution: Check your `GMAIL_CONNECTION_ID` exists in Nango

**Error: "Gmail connection test failed"**
- Solution: The connection might not have the right Gmail scopes

## Step 7: Project Structure

Your final project structure should look like:
```
gmail-nango-project/
├── .env                    # Your secrets (don't commit)
├── .gitignore             # Git ignore file
├── gmail_client.py        # Main Gmail client code
├── test_connection.py     # Test script
├── requirements.txt       # Python dependencies
└── venv/                  # Virtual environment (don't commit)
```

## Step 8: Using the Client in Your Code

### Basic usage example:
```python
from gmail_client import authenticate_gmail_with_nango
import os

# Get connection details from environment
connection_id = os.getenv('GMAIL_CONNECTION_ID')
provider_key = os.getenv('NANGO_PROVIDER_CONFIG_KEY')

# Authenticate
service = authenticate_gmail_with_nango(connection_id, provider_key)

# List recent emails
messages = service.users().messages().list(
    userId='me', 
    maxResults=10
).execute()

print(f"Found {len(messages.get('messages', []))} messages")

# Get first message details
if messages.get('messages'):
    msg_id = messages['messages'][0]['id']
    message = service.users().messages().get(
        userId='me', 
        id=msg_id
    ).execute()
    
    # Get headers
    headers = {h['name']: h['value'] for h in message['payload']['headers']}
    print(f"Subject: {headers.get('Subject', 'No subject')}")
    print(f"From: {headers.get('From', 'Unknown sender')}")
```

## Troubleshooting

### Debug mode
Add this to see the Nango response structure:
```python
def authenticate_gmail_with_nango_debug(connection_id: str, provider_config_key: str = "google"):
    """Debug version that shows Nango response"""
    nango_response = get_connection_credentials(connection_id, provider_config_key)
    
    print("=== NANGO RESPONSE DEBUG ===")
    print(f"Response keys: {list(nango_response.keys())}")
    print(f"Full response: {nango_response}")
    print("=== END DEBUG ===")
    
    # Continue with normal authentication...
```

### Test Nango connection directly
```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_nango_direct():
    base_url = os.getenv('NANGO_NANGO_BASE_URL')
    secret_key = os.getenv('NANGO_NANGO_SECRET_KEY')
    connection_id = os.getenv('GMAIL_CONNECTION_ID')
    
    url = f"{base_url}/connection/{connection_id}"
    headers = {"Authorization": f"Bearer {secret_key}"}
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

test_nango_direct()
```

This should get you up and running! Let me know if you encounter any specific errors.