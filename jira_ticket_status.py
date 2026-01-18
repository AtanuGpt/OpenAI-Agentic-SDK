import requests
import json
from agents import function_tool

@function_tool
async def fetch_ticket_status(ticket_key: str) -> dict:
    """
    Fetch the current status of an existing Jira ticket.

    Makes a synchronous HTTP POST request using the requests library
    with the ticket key passed in the request body.
    """

    url = "<<Your Azure Get Ticket Status Logic App Endpoint>>"
 
    payload = {
        "ticketKey": ticket_key
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        #print("➡️ Sending POST request with payload:", payload)

        response = requests.post(
            url,
            json=payload,       
            headers=headers,
            timeout=30
        )

        #print("⬅️ HTTP Status:", response.status_code)
        #print("⬅️ Raw Response:", response.text)

        if response.status_code != 200:
            return {
                "error": "Failed to fetch ticket status",
                "http_status": response.status_code,
                "details": response.text
            }

        return response.text

    except requests.exceptions.RequestException as ex:
        return {
            "error": "HTTP request failed",
            "details": str(ex)

        }
