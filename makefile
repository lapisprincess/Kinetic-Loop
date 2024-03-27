run:
	python3 src/main.py

clean:
	rm -r */__pycache__

setup: requirements.txt
	pip install pygame


nofov:
	python3 src/main.py stg nofov

noents:
	python3 src/main.py stg noents

nofov-noents:
	python3 src/main.py stg nofov noents

stg:
	python3 src/main.py stg



tile-sampler:
	python3 src/util/tile_sampler.py
