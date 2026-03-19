"""
Automatischer Email-Responder für clawy.studio@gmail.com
Prüft Inbox und antwortet auf Kaufanfragen
"""
import imaplib, smtplib, email as emaillib, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

EMAIL = "clawy.studio@gmail.com"
APP_PASSWORD = "wggrquwmvqremptw"
PRODUCT_PATH = "/home/node/.openclaw/workspace/projects/gumroad/ha-starter-kit.zip"

KEYWORDS_BUY = ["buy", "purchase", "starter kit", "payment", "order", "paypal", "kauf", "bestellen"]
KEYWORDS_SUPPORT = ["help", "question", "support", "hilfe", "frage"]

REPLY_BUY = """Hi there! 🏠

Thanks for your interest in the Home Assistant Starter Kit!

Here's how to get it:

**Option 1 - PayPal:**
Send $9 to: clawy.studio@gmail.com (PayPal)
Subject: "HA Starter Kit"
→ I'll send you the download link within 1 hour!

**Option 2 - Bank Transfer:**
Reply to this email and I'll send you my bank details.

What's included:
✅ dashboard.yaml - ready-to-use Lovelace dashboard
✅ automations.yaml - 4 essential automations
✅ setup guide - best integrations & tips for 2025

Any questions? Just reply to this email!

Cheers,
Clawy Studio
clawy.studio@gmail.com
https://schlapphome.uk/local/shop.html
"""

REPLY_SUPPORT = """Hi!

Thanks for reaching out to Clawy Studio! 🏠

I'll get back to you within 24 hours with a detailed answer.

In the meantime, check out our Home Assistant resources:
👉 https://schlapphome.uk/local/shop.html

Cheers,
Clawy Studio
"""

def check_and_reply():
    print(f"Checking inbox at {time.strftime('%H:%M:%S')}...")
    
    # Connect to inbox
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL, APP_PASSWORD)
    mail.select('inbox')
    
    # Get unread emails
    _, messages = mail.search(None, 'UNSEEN')
    ids = messages[0].split()
    
    if not ids:
        print("No new emails.")
        mail.logout()
        return
    
    print(f"Found {len(ids)} unread email(s)")
    
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(EMAIL, APP_PASSWORD)
    
    for msg_id in ids:
        _, msg_data = mail.fetch(msg_id, '(RFC822)')
        msg = emaillib.message_from_bytes(msg_data[0][1])
        
        sender = msg['From']
        subject = msg['Subject'] or ""
        
        # Get body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        content = (subject + " " + body).lower()
        print(f"From: {sender} | Subject: {subject[:50]}")
        
        # Skip if from ourselves
        if EMAIL in sender:
            continue
        
        # Determine reply type
        if any(kw in content for kw in KEYWORDS_BUY):
            reply_text = REPLY_BUY
            reply_subject = f"Re: {subject} - Payment Details 🏠"
            print(f"→ Sending BUY reply to {sender}")
        elif any(kw in content for kw in KEYWORDS_SUPPORT):
            reply_text = REPLY_SUPPORT
            reply_subject = f"Re: {subject}"
            print(f"→ Sending SUPPORT reply to {sender}")
        else:
            reply_text = REPLY_SUPPORT
            reply_subject = f"Re: {subject}"
            print(f"→ Sending generic reply to {sender}")
        
        # Send reply
        reply = MIMEMultipart()
        reply['From'] = f"Clawy Studio <{EMAIL}>"
        reply['To'] = sender
        reply['Subject'] = reply_subject
        reply.attach(MIMEText(reply_text, 'plain'))
        
        smtp.sendmail(EMAIL, sender, reply.as_string())
        print(f"✅ Reply sent to {sender}")
        
        # Mark as read
        mail.store(msg_id, '+FLAGS', '\\Seen')
    
    smtp.quit()
    mail.logout()

if __name__ == "__main__":
    check_and_reply()
