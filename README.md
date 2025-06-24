# Gmail MCP Server

A Model Context Protocol (MCP) server that provides Gmail functionality through FastMCP. This project allows you to interact with Gmail using MCP, enabling seamless integration with other MCP-compatible systems.

## What is this?

This is a Gmail MCP server that provides programmatic access to Gmail functionality. It uses FastMCP for server implementation and Nango for authentication. The server exposes various Gmail operations through MCP endpoints.

## Project Structure

```
gmail-mcp/
├── .env                    # Environment variables
├── .env.example           # Example environment file
├── gmail_auth.py          # Gmail authentication logic
├── gmail_mcp_server.py    # Main MCP server implementation
├── gmail_operations.py    # Gmail operation implementations
├── test_connection.py     # Test script
├── pyproject.toml         # Project configuration
└── uv.lock               # Dependency lock file
```

## Requirements

- Python 3.8+
- FastMCP
- Nango account (for authentication)
- Google Cloud Project with Gmail API enabled

## How to Run

1. Install dependencies:
```bash
# Install dependencies using uv
uv pip install .
```

2. Configure environment:
- Copy `.env.example` to `.env`
- Fill in your Nango credentials and Gmail connection details

3. Start the server:
```bash
python gmail_mcp_server.py
```

## Development Setup

To set up your development environment:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e .

# Run tests
uv pip install pytest
pytest test_connection.py
```

## MCP Server Implementation Details

### Core MCP Features

1. **Protocol Implementation**
   - Implements MCP 1.0 specification
   - Uses FastMCP for server implementation
   - Supports synchronous and asynchronous operations

2. **Context Management**
   - Maintains Gmail context state
   - Handles context switching
   - Preserves connection state

3. **Operation Types**
   - Query operations (search, list)
   - Mutation operations (send, update)
   - Batch operations support

### MCP Operation Example
```python
# Example MCP operation flow
context_id = "user_123_gmail"
operation_id = "send_email_456"

# Initialize operation
mcp.init_operation(operation_id, context_id)

# Execute operation
result = mcp.execute_operation(
    operation_id,
    {
        "type": "send_email",
        "data": {
            "to": "recipient@example.com",
            "subject": "Test Email",
            "body": "Hello!"
        }
    }
)

# Handle result
if result.success:
    print("Email sent successfully")
else:
    print(f"Error: {result.error}")
```

### MCP Integration Points

1. **Authentication Flow**
   - Nango OAuth2 integration
   - Token refresh handling
   - Multi-account support

2. **Error Handling**
   - Standardized error codes
   - Detailed error messages
   - Retry mechanisms

3. **Performance**
   - Connection pooling
   - Caching strategies
   - Batch operations

### Best Practices

1. **Connection Management**
   - Use connection pooling
   - Implement timeouts
   - Handle connection failures

2. **Error Recovery**
   - Implement retry logic
   - Handle partial failures
   - Monitor error rates

3. **Security**
   - Validate all inputs
   - Handle sensitive data
   - Implement proper access controls

### Common Use Cases

1. **Email Automation**
   - Automated sending
   - Template-based emails
   - Scheduled operations

2. **Email Processing**
   - Automated filtering
   - Rule-based processing
   - Batch operations

3. **Integration**
   - Connect with other MCP services
   - Create email workflows
   - Build email applications

### Troubleshooting

1. **Common Issues**
   - Connection timeouts
   - Authentication failures
   - Rate limiting

2. **Debugging Tips**
   - Enable debug logging
   - Check connection status
   - Monitor error codes

### Version Compatibility

- MCP Protocol: 1.0
- FastMCP: Latest stable
- Python: 3.8+
- Google API Client: Latest stable

### Security Considerations

1. **Authentication**
   - Secure OAuth2 flow
   - Token storage
   - Proper error handling

2. **Data Handling**
   - Input validation
   - Sensitive data handling
   - Error logging

3. **Rate Limiting**
   - API quotas
   - Usage monitoring
   - Error handling

### Performance Optimization

1. **Connection Pooling**
   - Reuse connections
   - Handle timeouts
   - Connection failures

2. **Caching**
   - Data caching
   - Operation results
   - Connection state

3. **Batch Operations**
   - Combine operations
   - Reduce API calls
   - Improve performance

### Monitoring and Logging

1. **Logging**
   - Operation logging
   - Error tracking
   - Performance metrics

2. **Metrics**
   - API usage
   - Performance
   - Error rates

3. **Alerting**
   - Critical errors
   - Performance issues
   - Usage patterns

### Future Enhancements

1. **Features**
   - Advanced filtering
   - More operations
   - Enhanced integration

2. **Performance**
   - Improved caching
   - Better connection handling
   - Optimized operations

3. **Security**
   - Enhanced authentication
   - Better error handling
   - Improved monitoring

### Community and Support

1. **Getting Help**
   - Documentation
   - Issue tracking
   - Community forums

2. **Contributing**
   - Code guidelines
   - Testing requirements
   - Documentation updates

### Advanced Topics

1. **Custom Operations**
   - Custom email processing
   - Advanced filtering
   - Complex workflows

2. **Integration Patterns**
   - Complex workflows
   - State management
   - Error handling

3. **Performance**
   - Optimization strategies
   - Scalability
   - Best practices

### Best Practices for MCP Integration

1. **Code Organization**
   - Separation of concerns
   - Proper abstractions
   - SOLID principles

2. **Error Handling**
   - Proper error handling
   - Retry mechanisms
   - Error logging

3. **Performance**
   - Optimization
   - Caching
   - Connection management

## Environment Variables

The following environment variables must be set:

```
NANGO_NANGO_BASE_URL=https://api.nango.dev
NANGO_NANGO_SECRET_KEY=your_nango_secret_key
GMAIL_CONNECTION_ID=your_gmail_connection_id
NANGO_PROVIDER_CONFIG_KEY=google
```

## Testing

Run the test script to verify your setup:
```bash
python test_connection.py
```

## Additional Notes

1. **Security**
   - Never commit `.env` file with credentials
   - Use `.env.example` as template
   - Keep API keys and secrets secure

2. **Dependencies**
   - Uses FastMCP for MCP implementation
   - Uses Nango for OAuth2 authentication
   - Uses Google API client for Gmail operations

3. **Development**
   - Requires Python virtual environment
   - Uses Poetry for dependency management
   - Follows PEP 8 style guidelines

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.

## Acknowledgments

- FastMCP for MCP implementation
- Nango for OAuth2 authentication
- Google API Python Client for Gmail operations
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