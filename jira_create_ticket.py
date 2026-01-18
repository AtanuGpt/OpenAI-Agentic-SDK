import requests
from agents import function_tool

@function_tool
async def create_ticket(
    subject: str,
    description: str,
    requestedby: str
) -> dict:
    """
    Create a new Jira ticket.

    Use this tool when the user wants to create, raise, or log a new ticket
    and provides the required ticket details.
    """

    url = "<<Your Azure Create Ticket Logic App Endpoint>>"

    payload = {
        "subject": subject,
        "description": description,
        "requestedby": requestedby
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            url,
            json=payload,   
            headers=headers,
            timeout=30
        )

        if response.status_code not in (200, 201):
            return {
                "error": "Failed to create ticket",
                "http_status": response.status_code,
                "details": response.text
            }

        return response.text

    except requests.exceptions.RequestException as ex:
        return {
            "error": "HTTP request failed",
            "details": str(ex)
        }

