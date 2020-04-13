# Makefile

SHELL:=/bin/bash
# Running development server
run:
	source label/bin/activate
	python main.py

# Install depencencies
install: 
	pip install virtualenv
	virtualenv label 
	source label/bin/activate
	pip -r requirements.txt

# Add new dependency
update:
	pip freeze > requirements.txt
