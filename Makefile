# initialise l'environnement python
init-env:
	python -m venv venv

# installe les requis
install-requirements:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# lance l'application
launch-api:
	uvicorn api.api:app --reload --port 8000 --host 0.0.0.0
