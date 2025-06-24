"""
Gmail MCP Server

This module provides Gmail functionality through Model Context Protocol
using FastMCP for simplified server setup.
"""

import os
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Import our Gmail authentication and client
from gmail_auth import authenticate_gmail_with_nango_v2
from gmail_operations import GmailClient

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Gmail MCP Server")

# Global variables for Gmail connection
_gmail_client: Optional[GmailClient] = None
_gmail_service = None


def get_gmail_client() -> GmailClient:
    """Get or create the global Gmail client."""
    global _gmail_client, _gmail_service
    
    if _gmail_client is None:
        connection_id = os.getenv('GMAIL_CONNECTION_ID')
        provider_config_key = os.getenv('NANGO_PROVIDER_CONFIG_KEY', 'google')
        
        if not connection_id:
            raise ValueError("GMAIL_CONNECTION_ID environment variable is required")
        
        print(f"Initializing Gmail client with connection: {connection_id}")
        _gmail_service = authenticate_gmail_with_nango_v2(connection_id, provider_config_key)
        _gmail_client = GmailClient(_gmail_service)
        print("Gmail client initialized successfully")
    
    return _gmail_client


def validate_message_id(message_id: str) -> bool:
    """Validate Gmail message ID format."""
    return bool(message_id and isinstance(message_id, str) and len(message_id) > 0)


def validate_email_address(email: str) -> bool:
    """Basic email validation."""
    return bool(email and '@' in email and '.' in email.split('@')[1])


@mcp.tool()
def gmail_list_messages(
    query: str = "",
    max_results: int = 10
) -> Dict[str, Any]:
    """
    List Gmail messages with optional search query.
    
    Args:
        query: Gmail search query (e.g., 'from:sender@example.com', 'is:unread')
        max_results: Maximum number of messages to return (1-100)
        
    Returns:
        Dictionary with success status and message data
    """
    try:
        # Validate parameters
        if max_results < 1 or max_results > 100:
            return {"success": False, "error": "max_results must be between 1 and 100"}
        
        gmail = get_gmail_client()
        messages = gmail.list_messages(query=query, max_results=max_results)
        
        if not messages:
            return {"success": True, "count": 0, "messages": [], "message": "No messages found"}
        
        # Get detailed info for each message
        detailed_messages = []
        for msg in messages:
            message = gmail.get_message(msg['id'])
            if message:
                headers = gmail.get_message_headers(message)
                detailed_messages.append({
                    'id': msg['id'],
                    'from': headers.get('From', 'Unknown'),
                    'subject': headers.get('Subject', 'No Subject'),
                    'date': headers.get('Date', 'Unknown'),
                    'snippet': message.get('snippet', '')[:100] + '...' if message.get('snippet') else '',
                    'labels': message.get('labelIds', []),
                    'is_unread': 'UNREAD' in message.get('labelIds', [])
                })
        
        return {
            "success": True,
            "count": len(detailed_messages),
            "messages": detailed_messages,
            "query_used": query or "all messages"
        }
        
    except Exception as e:
        return {"success": False, "error": f"Failed to list messages: {str(e)}"}


@mcp.tool()
def gmail_get_message(message_id: str) -> Dict[str, Any]:
    """
    Get details of a specific Gmail message.
    
    Args:
        message_id: Gmail message ID
        
    Returns:
        Dictionary with message details or error
    """
    try:
        if not validate_message_id(message_id):
            return {"success": False, "error": "Invalid message ID provided"}
        
        gmail = get_gmail_client()
        message = gmail.get_message(message_id)
        
        if not message:
            return {"success": False, "error": f"Message {message_id} not found"}
        
        headers = gmail.get_message_headers(message)
        body = gmail.get_message_body(message)
        
        return {
            "success": True,
            "message": {
                "id": message_id,
                "from": headers.get('From', 'Unknown'),
                "to": headers.get('To', 'Unknown'),
                "subject": headers.get('Subject', 'No Subject'),
                "date": headers.get('Date', 'Unknown'),
                "body": body,
                "snippet": message.get('snippet', ''),
                "labels": message.get('labelIds', []),
                "thread_id": message.get('threadId', ''),
                "is_unread": 'UNREAD' in message.get('labelIds', [])
            }
        }
        
    except Exception as e:
        return {"success": False, "error": f"Failed to get message: {str(e)}"}


@mcp.tool()
def gmail_send_message(
    to: str,
    subject: str,
    body: str,
    cc: str = "",
    bcc: str = ""
) -> Dict[str, Any]:
    """
    Send a Gmail message.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        cc: CC recipients (comma-separated)
        bcc: BCC recipients (comma-separated)
        
    Returns:
        Dictionary with send result
    """
    try:
        # Validate parameters
        if not validate_email_address(to):
            return {"success": False, "error": "Invalid recipient email address"}
        
        if not subject.strip():
            return {"success": False, "error": "Subject cannot be empty"}
        
        if not body.strip():
            return {"success": False, "error": "Body cannot be empty"}
        
        gmail = get_gmail_client()
        result = gmail.send_message(to=to, subject=subject, body=body)
        
        if result:
            return {
                "success": True,
                "message": "Email sent successfully",
                "message_id": result['id'],
                "to": to,
                "subject": subject
            }
        else:
            return {"success": False, "error": "Failed to send email"}
            
    except Exception as e:
        return {"success": False, "error": f"Failed to send message: {str(e)}"}


@mcp.tool()
def gmail_search_messages(
    sender: Optional[str] = None,
    subject: Optional[str] = None,
    after_date: Optional[str] = None,
    before_date: Optional[str] = None,
    has_attachment: bool = False,
    is_unread: bool = False,
    max_results: int = 20
) -> Dict[str, Any]:
    """
    Search Gmail messages with specific criteria.
    
    Args:
        sender: Filter by sender email
        subject: Filter by subject keywords
        after_date: Filter messages after date (YYYY/MM/DD format)
        before_date: Filter messages before date (YYYY/MM/DD format)
        has_attachment: Filter messages with attachments
        is_unread: Filter unread messages
        max_results: Maximum number of messages to return (1-100)
        
    Returns:
        Dictionary with search results
    """
    try:
        # Validate parameters
        if max_results < 1 or max_results > 100:
            return {"success": False, "error": "max_results must be between 1 and 100"}
        
        gmail = get_gmail_client()
        messages = gmail.search_messages(
            sender=sender,
            subject=subject,
            after_date=after_date,
            has_attachment=has_attachment,
            is_unread=is_unread
        )
        
        if not messages:
            return {
                "success": True,
                "count": 0,
                "messages": [],
                "message": "No messages found matching search criteria"
            }
        
        # Limit results
        messages = messages[:max_results]
        
        # Get detailed info for each message
        detailed_messages = []
        for msg in messages:
            message = gmail.get_message(msg['id'])
            if message:
                headers = gmail.get_message_headers(message)
                detailed_messages.append({
                    'id': msg['id'],
                    'from': headers.get('From', 'Unknown'),
                    'subject': headers.get('Subject', 'No Subject'),
                    'date': headers.get('Date', 'Unknown'),
                    'snippet': message.get('snippet', '')[:100] + '...' if message.get('snippet') else '',
                    'is_unread': 'UNREAD' in message.get('labelIds', []),
                    'has_attachment': 'attachment' in (message.get('snippet', '') or '').lower()
                })
        
        # Build search criteria summary
        criteria = []
        if sender: criteria.append(f"sender: {sender}")
        if subject: criteria.append(f"subject: {subject}")
        if after_date: criteria.append(f"after: {after_date}")
        if before_date: criteria.append(f"before: {before_date}")
        if has_attachment: criteria.append("has attachment")
        if is_unread: criteria.append("unread only")
        
        return {
            "success": True,
            "count": len(detailed_messages),
            "messages": detailed_messages,
            "search_criteria": criteria or ["all messages"]
        }
        
    except Exception as e:
        return {"success": False, "error": f"Failed to search messages: {str(e)}"}


@mcp.tool()
def gmail_mark_as_read(message_ids: List[str]) -> Dict[str, Any]:
    """
    Mark Gmail messages as read.
    
    Args:
        message_ids: List of message IDs to mark as read
        
    Returns:
        Dictionary with operation result
    """
    try:
        if not message_ids:
            return {"success": False, "error": "No message IDs provided"}
        
        # Validate message IDs
        invalid_ids = [msg_id for msg_id in message_ids if not validate_message_id(msg_id)]
        if invalid_ids:
            return {"success": False, "error": f"Invalid message IDs: {invalid_ids}"}
        
        gmail = get_gmail_client()
        success_count = 0
        failed_ids = []
        
        for msg_id in message_ids:
            if gmail.mark_as_read(msg_id):
                success_count += 1
            else:
                failed_ids.append(msg_id)
        
        result = {
            "success": success_count > 0,
            "marked_as_read": success_count,
            "total_requested": len(message_ids),
            "message": f"Marked {success_count}/{len(message_ids)} messages as read"
        }
        
        if failed_ids:
            result["failed_ids"] = failed_ids
        
        return result
        
    except Exception as e:
        return {"success": False, "error": f"Failed to mark messages as read: {str(e)}"}


@mcp.tool()
def gmail_delete_messages(message_ids: List[str]) -> Dict[str, Any]:
    """
    Delete Gmail messages.
    
    Args:
        message_ids: List of message IDs to delete
        
    Returns:
        Dictionary with operation result
    """
    try:
        if not message_ids:
            return {"success": False, "error": "No message IDs provided"}
        
        # Validate message IDs
        invalid_ids = [msg_id for msg_id in message_ids if not validate_message_id(msg_id)]
        if invalid_ids:
            return {"success": False, "error": f"Invalid message IDs: {invalid_ids}"}
        
        gmail = get_gmail_client()
        success_count = 0
        failed_ids = []
        
        for msg_id in message_ids:
            if gmail.delete_message(msg_id):
                success_count += 1
            else:
                failed_ids.append(msg_id)
        
        result = {
            "success": success_count > 0,
            "deleted": success_count,
            "total_requested": len(message_ids),
            "message": f"Deleted {success_count}/{len(message_ids)} messages"
        }
        
        if failed_ids:
            result["failed_ids"] = failed_ids
            result["warning"] = "Some messages could not be deleted"
        
        return result
        
    except Exception as e:
        return {"success": False, "error": f"Failed to delete messages: {str(e)}"}


@mcp.tool()
def gmail_get_stats(include_unread: bool = True) -> Dict[str, Any]:
    """
    Get Gmail account statistics.
    
    Args:
        include_unread: Include unread message count
        
    Returns:
        Dictionary with account statistics
    """
    try:
        gmail = get_gmail_client()
        
        # Get profile information
        profile = _gmail_service.users().getProfile(userId='me').execute()
        
        stats = {
            "success": True,
            "email_address": profile.get('emailAddress', 'Unknown'),
            "total_messages": profile.get('messagesTotal', 0),
            "total_threads": profile.get('threadsTotal', 0),
            "history_id": profile.get('historyId', 'Unknown')
        }
        
        if include_unread:
            try:
                unread_messages = gmail.search_messages(is_unread=True, max_results=100)
                stats["unread_count"] = len(unread_messages)
            except Exception as e:
                stats["unread_count"] = f"Error counting unread: {str(e)}"
        
        return stats
        
    except Exception as e:
        return {"success": False, "error": f"Failed to get stats: {str(e)}"}


@mcp.tool()
def gmail_send_message_with_attachment(
    to: str,
    subject: str,
    body: str,
    file_path: str,
    cc: str = ""
) -> Dict[str, Any]:
    """
    Send Gmail message with attachment.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        file_path: Path to file to attach
        cc: CC recipients (comma-separated)
        
    Returns:
        Dictionary with send result
    """
    try:
        # Validate parameters
        if not validate_email_address(to):
            return {"success": False, "error": "Invalid recipient email address"}
        
        if not subject.strip():
            return {"success": False, "error": "Subject cannot be empty"}
        
        if not body.strip():
            return {"success": False, "error": "Body cannot be empty"}
        
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}
        
        gmail = get_gmail_client()
        result = gmail.send_message_with_attachment(
            to=to, 
            subject=subject, 
            body=body, 
            file_path=file_path
        )
        
        if result:
            return {
                "success": True,
                "message": "Email with attachment sent successfully",
                "message_id": result['id'],
                "to": to,
                "subject": subject,
                "attachment": os.path.basename(file_path)
            }
        else:
            return {"success": False, "error": "Failed to send email with attachment"}
            
    except Exception as e:
        return {"success": False, "error": f"Failed to send message with attachment: {str(e)}"}


def main():
    try:
        print("Starting Gmail MCP Server...")
        mcp.run(transport="sse")
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"Server failed to start: {str(e)}")
        raise