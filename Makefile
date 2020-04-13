# Makefile

SHELL:=/bin/bash
# Running development server
run:
	python main.py

# Add new dependency
update:
	pip freeze > requirements.txt
