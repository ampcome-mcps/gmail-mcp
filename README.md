# Gmail MCP Server

A Model Context Protocol (MCP) server that provides comprehensive Gmail functionality through FastMCP. This server enables AI assistants like Claude to interact with Gmail accounts, manage emails, send messages, and perform various Gmail operations using OAuth2 authentication via Nango.

## Features

### Core Gmail Operations

- **Message Management**: List, search, read, and delete emails
- **Send Emails**: Send messages with or without attachments
- **Message Actions**: Mark messages as read, manage labels
- **Advanced Search**: Filter by sender, subject, date, attachments, read status
- **Account Statistics**: Get Gmail account overview and metrics
- **Thread Support**: Handle Gmail conversation threads
- **Attachment Support**: Send emails with file attachments

### Authentication & Security

- **OAuth2 Integration**: Secure authentication via Nango
- **Token Management**: Automatic token refresh and validation
- **Multi-account Support**: Handle multiple Gmail accounts
- **Secure Credential Storage**: Environment-based configuration

## Prerequisites

- Python 3.13+
- Gmail account with API access enabled
- Google Cloud Project with Gmail API enabled
- Nango account for OAuth2 management (optional but recommended)

## Installation

1. **Clone or create the project structure**:

```bash
mkdir gmail-mcp-server
cd gmail-mcp-server
```

2. **Create a virtual environment**:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -e .
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Nango Configuration (Recommended)
NANGO_BASE_URL=https://api.nango.dev
NANGO_SECRET_KEY=your_nango_secret_key
NANGO_CONNECTION_ID=your_NANGO_CONNECTION_ID
NANGO_INTEGRATION_ID=google

# Alternative: Direct Google OAuth (if not using Nango)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REFRESH_TOKEN=your_refresh_token
```

### Google Cloud Setup

1. **Create a Google Cloud Project**:

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Gmail API**:

   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it

3. **Create OAuth2 Credentials**:

   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application" or "Web application"
   - Note the Client ID and Client Secret

4. **Configure OAuth Scopes**:
   - Add the following scopes:
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.send`
     - `https://www.googleapis.com/auth/gmail.modify`

### Nango Setup (Recommended)

1. **Create Nango Account**: Sign up at [nango.dev](https://nango.dev)
2. **Create Google Integration**: Set up Google OAuth2 integration
3. **Configure Connection**: Create a connection for your Gmail account
4. **Get Credentials**: Note your connection ID and provider config key

### Claude Desktop Configuration

Add this configuration to your Claude Desktop config file:

**Location**:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

#### With Nango

```json
{
  "mcpServers": {
    "gmail": {
      "command": "uvx",
      "args": ["git+https://github.com/Shameerpc5029/gmail-mcp.git"],
      "env": {
        "NANGO_BASE_URL": "https://api.nango.dev",
        "NANGO_SECRET_KEY": "your_nango_secret_key",
        "NANGO_CONNECTION_ID": "your_nango_connection_id",
        "NANGO_INTEGRATION_ID": "google-mail"
      }
    }
  }
}
```

**Notes**:

- On Windows, use backslashes in paths: `C:\\path\\to\\your\\gmail-mcp-server\\main.py`
- For virtual environment on Windows: `.venv\\Scripts\\python.exe`
- Replace placeholder values with your actual credentials

## Available Tools

The MCP server provides the following tools for Claude:

### Message Operations

- `gmail_list_messages` - List Gmail messages with optional search query
- `gmail_get_message` - Get details of a specific message
- `gmail_search_messages` - Advanced search with multiple criteria
- `gmail_send_message` - Send a new email message
- `gmail_send_message_with_attachment` - Send email with file attachment

### Message Management

- `gmail_mark_as_read` - Mark messages as read
- `gmail_delete_messages` - Delete messages permanently

### Account Information

- `gmail_get_stats` - Get Gmail account statistics and overview

## Usage Examples

Once configured with Claude, you can use natural language commands like:

### Basic Operations

- "Show me my latest 10 emails"
- "Search for emails from john@example.com sent this week"
- "Get the full content of message ID xyz123"
- "Send an email to sarah@example.com with subject 'Meeting Tomorrow'"

### Advanced Operations

- "Find all unread emails with attachments from the last 7 days"
- "Mark all emails from newsletter@company.com as read"
- "Delete the email with ID abc456"
- "Send a report to my manager with the quarterly-report.pdf attachment"
- "Show me my Gmail account statistics"

### Search Capabilities

- "Find emails about 'project alpha' from last month"
- "Show unread emails from important@client.com"
- "List emails with attachments sent after 2024/01/01"

## Project Structure

```
gmail-mcp-server/
├── main.py                 # FastMCP server implementation
├── gmail_auth.py           # Gmail OAuth2 authentication
├── gmail_operations.py     # Gmail client operations
├── pyproject.toml         # Project configuration
├── .env                   # Environment variables (create from template)
├── .env.example          # Environment template
├── README.md             # This file
├── uv.lock              # Dependency lock file
└── .gitignore           # Git ignore rules
```

## Running the Server

### With Claude Desktop

The server automatically starts when Claude Desktop loads the configuration.

### Standalone Testing

For development and testing:

```bash
python main.py
```

## Tool Specifications

### gmail_list_messages

```python
# Parameters:
- query: str = ""              # Gmail search query
- max_results: int = 10        # Max messages (1-100)

# Returns:
{
  "success": bool,
  "count": int,
  "messages": [
    {
      "id": "message_id",
      "from": "sender@example.com",
      "subject": "Email subject",
      "date": "2024-01-01",
      "snippet": "Preview text...",
      "is_unread": bool
    }
  ]
}
```

### gmail_search_messages

```python
# Parameters:
- sender: str = None           # Filter by sender
- subject: str = None          # Filter by subject
- after_date: str = None       # After date (YYYY/MM/DD)
- before_date: str = None      # Before date (YYYY/MM/DD)
- has_attachment: bool = False # Filter with attachments
- is_unread: bool = False      # Filter unread only
- max_results: int = 20        # Max results (1-100)
```

### gmail_send_message

```python
# Parameters:
- to: str                      # Recipient email (required)
- subject: str                 # Email subject (required)
- body: str                    # Email content (required)
- cc: str = ""                # CC recipients
- bcc: str = ""               # BCC recipients

# Returns:
{
  "success": bool,
  "message_id": "sent_message_id",
  "to": "recipient@example.com",
  "subject": "Email subject"
}
```

## Development

### Key Components

1. **main.py**: FastMCP server with tool definitions
2. **gmail_auth.py**: OAuth2 authentication handling
3. **gmail_operations.py**: Gmail API client wrapper
4. **Nango Integration**: Secure credential management

### Adding New Features

1. **Add Gmail Operation**: Extend `GmailClient` class in `gmail_operations.py`
2. **Define MCP Tool**: Add `@mcp.tool()` decorator in `main.py`
3. **Add Validation**: Include parameter validation and error handling
4. **Update Documentation**: Add usage examples and tool specifications

### Dependencies

- `google-api-python-client` - Official Google API client
- `google-auth` - Google authentication library
- `mcp[cli]` - Model Context Protocol framework
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation
- `requests` - HTTP client for Nango integration

## Troubleshooting

### Common Issues

1. **Authentication Errors**:

   - Verify Nango credentials are correct
   - Check Gmail API is enabled in Google Cloud
   - Ensure OAuth scopes are properly configured

2. **Permission Errors**:

   - Verify OAuth2 scopes include required permissions
   - Check if Gmail account has necessary access

3. **Message Not Found**:

   - Ensure message IDs are valid Gmail message IDs
   - Check if messages haven't been deleted

4. **Rate Limiting**:
   - Gmail API has quotas and rate limits
   - Implement retry logic for production use

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export GMAIL_MCP_DEBUG=true
```

### Testing Nango Connection

```python
# Test script to verify Nango setup
from gmail_auth import get_connection_credentials

try:
    result = get_connection_credentials("your_connection_id", "google")
    print("Nango connection successful:", result.keys())
except Exception as e:
    print("Nango connection failed:", e)
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` files with credentials
2. **Token Storage**: Tokens are handled securely by Nango
3. **API Quotas**: Monitor Gmail API usage to avoid quota exhaustion
4. **Scope Limitations**: Use minimal required OAuth scopes
5. **Access Control**: Limit MCP server access to authorized clients

## Performance Optimization

1. **Batch Operations**: Use batch requests when possible
2. **Caching**: Implement message caching for frequently accessed data
3. **Pagination**: Handle large result sets with proper pagination
4. **Connection Pooling**: Reuse HTTP connections for API calls

## Error Handling

The server implements comprehensive error handling:

- **Validation Errors**: Parameter validation with descriptive messages
- **API Errors**: Gmail API error handling and retry logic
- **Authentication Errors**: Token refresh and re-authentication
- **Network Errors**: Connection timeout and retry mechanisms

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Check the [troubleshooting section](#troubleshooting)
- Review Gmail API documentation: [Gmail API Guide](https://developers.google.com/gmail/api)
- Open an issue in the project repository
- Check Nango documentation: [Nango Docs](https://docs.nango.dev)

## Acknowledgments

- **FastMCP**: Simplified MCP server implementation
- **Google API Python Client**: Official Gmail API integration
- **Nango**: OAuth2 authentication management
- **Model Context Protocol**: Standard for AI tool integration
