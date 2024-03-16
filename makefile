run:
	python3 src/main.py

clean:
	rm -r */__pycache__

nofov:
	python3 src/main.py nofov

testroom:
	python3 src/main.py testroom

nofov-testroom:
	python3 src/main.py nofov testroom


tile-sampler:
	python3 src/util/tile_sampler.py


setup: requirements.txt
	pip install pygame
