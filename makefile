run:
	python3 src/main.py

clean:
	rm -r */__pycache__

setup: requirements.txt
	pip install pygame


nofov:
	python3 src/main.py nofov

testroom:
	python3 src/main.py testroom

nofov-testroom:
	python3 src/main.py nofov testroom

stg:
	python3 src/main.py stg



tile-sampler:
	python3 src/util/tile_sampler.py
