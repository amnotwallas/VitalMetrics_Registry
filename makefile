install:
	pip install -r requirements.txt

run_api:
	uvicorn app.main:app --reload

## docs http://127.0.0.1:8000/docs