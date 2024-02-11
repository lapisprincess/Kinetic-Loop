run:
	python3 src/main.py

tile-sampler:
	python3 src/util/graphic.py tile_sampler 0 0

setup: requirements.txt
	pip install pygame

clean:
	rm -rf src/__pycache__

