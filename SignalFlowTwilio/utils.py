import frappe
from twilio.rest import Client

@frappe.whitelist()
def send_sms(to, message_body):
    settings = frappe.get_single("Twilio Settings")

    client = Client(
        settings.account_sid,
        settings.get_password("auth_token")
    )

    message = client.messages.create(
        body=message_body,
        from_=settings.from_number,
        to=to
    )

    return message.sid

import frappe
from twilio.rest import Client


@frappe.whitelist()
def make_call(to):

    settings = frappe.get_single("Twilio Settings")

    client = Client(
        settings.account_sid,
        settings.get_password("auth_token")
    )

    # YOUR number (verified number)
    your_number = "+919326209116"

    voice_url = (
        settings.ngrok_url
        + "/api/method/twilio_integration.utils.voice_bridge?to="
        + to
    )

    call = client.calls.create(
        to=your_number,
        from_=settings.from_number,
        url=voice_url
    )

    return call.sid

import frappe
from twilio.twiml.voice_response import VoiceResponse
from frappe.utils.response import Response


@frappe.whitelist(allow_guest=True)
def voice_bridge(to=None):

    settings = frappe.get_single("Twilio Settings")

    # Clean number
    to = to.replace(" ", "")

    # Only add +91 if missing
    if not to.startswith("+"):
        to = "+" + to

    from_number = settings.from_number.replace(" ", "")

    response = VoiceResponse()

    response.dial(
        to,
        callerId=from_number
    )

    return Response(
        str(response),
        content_type="text/xml"
    )
