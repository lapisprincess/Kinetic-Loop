run:
	python3 src/main.py

setup: requirements.txt
	pip install pygame

clean:
	rm -rf src/__pycache__

