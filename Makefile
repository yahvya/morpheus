# initialise l'environnement virtuel
init-env:
	python3 -m venv venv

# lance l'environnement sous windows
active-windows-env:
	./venv/Scripts/ctivate

# lance l'environnement sous mac
active-mac-env:
	source ./venv/bin/activate

# désactive l'environnement sous windows
disable-windows-env:
	.\venv\Scripts\deactivate

# installe les requis windows
install-requirements-windows: init-env active-windows-env
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# installe les requis mac
install-requirements-mac: init-env active-mac-env
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# lance l'application
launch-app:
	uvicorn api.api:app --reload

# lance l'application sous windows
launch-app-windows: disable-windows-env active-windows-env launch-app

# lance l'application sous mac
launch-app-mac: active-mac-env launch-app

