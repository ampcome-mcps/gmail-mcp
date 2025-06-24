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