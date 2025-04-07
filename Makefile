run:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000

celery:
	poetry run celery -A tasks.tasks.celery_app worker --loglevel=info

celery-beat:
	poetry run celery -A tasks.tasks.celery_app beat --loglevel=info

migrate:
	poetry run alembic upgrade head