import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scraper import FeedItem

def send_notification(item: FeedItem):
    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_username = os.environ["SMTP_USERNAME"]
    smtp_password = os.environ["SMTP_PASSWORD"]
    notify_email = os.environ["NOTIFY_EMAIL"]
    subject = f"🐱 Kitten Watch: {item.title}"
    image_html = f'<p><img src="{item.image_url}" style="max-width:480px;border-radius:8px"/></p>' if item.image_url else ""
    snippet = item.description_text[:800].replace("\n", "<br>")
    html_body = f"""<html><body style="font-family:sans-serif;max-width:600px;margin:auto">
        <h2 style="color:#b45309">🐱 {item.title}</h2>
        {image_html}
        <p style="color:#555;font-size:0.85em">Posted: {item.pub_date}</p>
        <div style="background:#fefce8;border-left:4px solid #b45309;padding:12px;border-radius:4px">{snippet}</div>
        <p><a href="{item.link}" style="color:#b45309;font-weight:bold">View full post →</a></p>
        <p style="font-size:0.75em;color:#aaa">Sent by Kitten Watch 🐾</p>
    </body></html>"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_username
    msg["To"] = notify_email
    msg.attach(MIMEText(html_body, "html"))
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo(); server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, notify_email, msg.as_string())
    print(f"  ✉️  Email sent for: {item.title}")
