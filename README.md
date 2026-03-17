# AutoBizOps

A web-based automation platform that helps businesses automate repetitive operations, starting with AI-powered blog post generation via N8N workflows.

## Features

- **AI Blog Post Generator** — Submit a keyword, niche, target audience, and personal take; an N8N webhook + Celery worker generates a full blog post asynchronously
- **Custom Automation Requests** — Submit automation ideas for custom quotes
- **User Accounts** — Registration, login, and a personal dashboard showing all generated content
- **Credit System** — Users receive 25 free credits on signup; each automation costs credits
- **Async Processing** — Celery workers on Redis handle long-running generation tasks in the background
- **Iteration Tracking** — Multiple versions of generated posts are stored and viewable

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask 3.1, SQLAlchemy, Flask-Login, Flask-Migrate |
| Task Queue | Celery 5.5 with Redis broker |
| Database | PostgreSQL |
| Frontend | Jinja2 templates, Bootstrap 5, DataTables, jQuery |
| External | N8N webhook workflows for content generation |
| Testing | Pytest |

## Project Structure

```
autobizops/
├── __init__.py              # App factory, config, Celery setup
├── models.py                # SQLAlchemy models (User, Automation, BlogPost, etc.)
├── apps/
│   ├── blog_generator/      # Blog generation feature (views, forms)
│   └── custom_automation/   # Custom automation request form
├── core/                    # Landing pages (index, about, pricing)
├── users/                   # Auth routes (register, login, account)
├── celery/                  # Async task definitions
├── templates/               # Jinja2 HTML templates
├── static/                  # CSS, icons
├── error_pages/             # Error handlers
└── tests/                   # Pytest test suite
```

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis

### Setup

```bash
# Clone the repo
git clone https://github.com/<your-username>/AutoBizOps.git
cd AutoBizOps

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy the example env file and fill in your values
cp .env.example .env

# Run database migrations
flask db upgrade
```

### Running

```bash
# Start Redis (if not already running)
redis-server

# Start the Celery worker (in a separate terminal)
celery -A autobizops.celery_app worker --loglevel=info

# Start the Flask dev server
python app.py
```

The app will be available at `http://localhost:5000`.

### Optional: Celery monitoring

```bash
celery -A autobizops.celery_app flower
```

## Environment Variables

See [`.env.example`](.env.example) for all required variables:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for session signing |
| `DATABASE_URL` | PostgreSQL connection string |
| `CELERY_BROKER_URL` | Redis URL for Celery broker |
| `CELERY_RESULT_BACKEND` | Redis URL for Celery results |
| `N8N_BLOG_GENERATION_WEBHOOK_URL` | N8N webhook endpoint for blog generation |

## Running Tests

```bash
pytest
```

## License

This project is for portfolio/demonstration purposes.
