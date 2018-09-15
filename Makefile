all:

build:
	docker-compose build

up:	build
	docker-compose up

test: build
	docker-compose run web pytest

fix:
	autopep8 --in-place --recursive .