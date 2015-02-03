# You should consider overriding or inheriting these,
# from the .ini file
SSH_USERNAME = odin
SSH_HOST = newstaging.bachvarov.info
FAB_FOLDER = deploy_tools

all: help

help:
	@echo ""
	@echo "Your current settings are: $(SSH_USERNAME)@$(SSH_HOST)"
	@echo "Available commands:"
	@echo "make clean         - removes *.pyc files"
	@echo "make help          - this help info"
	@echo "make pip-update    - updates current virtualenv's python packages"
	@echo "make deploy-update - deploys to production"
	@echo ""

clean:
	rm -rf *~*
	find . -name '*.pyc' -exec rm {} \;

pip-update:
	PIP_REQUIRE_VIRTUALENV=true
	pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U

deploy-update:
	cd $(FAB_FOLDER);fab -f fabfile.py -H $(SSH_USERNAME)@$(SSH_HOST) update



.PHONY: help clean pip-update deploy-update
