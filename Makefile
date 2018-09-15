all:

up:
	docker-compose build
	docker-compose up

fix:
	autopep8 --in-place --recursive .