# You should consider overriding or inheriting these,
# from the .ini file
SSH_USERNAME = {{ USERNAME }}
SSH_HOST = {{ HOST }}
SOURCE_FOLDER = sites/{{ DOMAIN }}/source
GUNICORN_UPSTART_JOB = gunicorn-{{ DOMAIN }}.conf

clean:
	rm -rf *~*
	find . -name '*.pyc' -exec rm {} \;

pip-update:
	pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U

deploy-update:
	ssh $(USERNAME)@$(HOST)
	cd $(SOURCE_FOLDER)
	git pull origin master --rebase --quiet
	sudo service nginx restart
	sudo restart $(GUNICORN_UPSTART_JOB)



.PHONY: clean pip-update deploy-update
