# You should consider overriding or inheriting these,
# from the .ini file
SSH_USERNAME = {{ USERNAME }}
SSH_HOST = {{ HOST }}
FAB_FOLDER = deploy_tools


all: help

help:
	@echo 'Available commands are:'
	@echo 'clean, pip-update and deploy-update'

clean:
	rm -rf *~*
	find . -name '*.pyc' -exec rm {} \;

pip-update:
	PIP_REQUIRE_VIRTUALENV=true
	pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U

deploy-update:
	cd $(FAB_FOLDER);fab -f fabfile.py -H $(SSH_USERNAME)@$(SSH_HOST) update



.PHONY: all clean pip-update deploy-update
