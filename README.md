# 🐾 Kitten Watch

Monitors the Heronbank Cat Rescue Facebook group RSS feed and emails you when
new kitten listings appear.

## Local dev
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export DATABASE_URL="postgresql://user:password@localhost:5432/kittenwatch"
export RSS_FEED_URL="https://rss.app/feeds/8ZEez9pneLj9S3q2.xml"
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="you@gmail.com"
export SMTP_PASSWORD="your-app-password"
export NOTIFY_EMAIL="you@gmail.com"

python main.py
```

Gmail App Password: myaccount.google.com → Security → 2-Step Verification → App Passwords

## Deploy to Render

1. Push to GitHub
2. Render dashboard → New → Blueprint → connect repo
3. Render picks up render.yaml and creates the DB + cron job
4. Set SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, NOTIFY_EMAIL in the cron job Environment tab
5. Hit "Trigger Run" to test

## Customise

- Keywords: edit MATCH_KEYWORDS in filter.py
- Schedule: edit the cron expression in render.yaml
- More sources: add feed URLs to a list in main.py
