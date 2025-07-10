import yagmail
from datetime import datetime
from config.settings import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT

def notify_error(message: str) -> None:
    """
    Sends an email notification if a job fails.

    Args:
        message (str): The error message to include in the email body.
    """
    subject = "🚨 Global Market Pulse Alert"
    body = f"""
    An error occurred during the scheduled job:

    {message}

    Timestamp: {datetime.now()}
    """

    try:
        yag = yagmail.SMTP(user=EMAIL_SENDER, password=EMAIL_PASSWORD)
        yag.send(to=EMAIL_RECIPIENT, subject=subject, contents=body)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Email alert failed:", e)
