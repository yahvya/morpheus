init-env:
	python -m venv venv

install-requirements:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

launch-api:
	uvicorn api:app --reload --port 8000 --host 0.0.0.0