# Makefile

SHELL:=/bin/bash
# Running development server
run:
	source label/bin/activate
	python3 main.py

# Install depencencies
install: 
	virtualenv label 
	source label/bin/activate
	pip install -r requirements.txt

# Add new dependency
update:
	pip freeze > requirements.txt
