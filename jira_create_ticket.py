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

    url = "https://prod-26.centralindia.logic.azure.com:443/workflows/82b73d48b5714812bdc391fecdaf5b43/triggers/When_an_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_an_HTTP_request_is_received%2Frun&sv=1.0&sig=MG_MfLwxw7HoBq5o59KwMm_0RyieZN3pepEgO3iSChc"

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
