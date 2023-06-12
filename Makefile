run:
	poetry run uvicorn main:app --reload

lint:
	poetry run flake8 courses data grades students teachers main.py