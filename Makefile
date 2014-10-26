clean:
	rm -rf *~*
	find . -name '*.pyc' -exec rm {} \;

pip-update:
	pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U


.PHONY: clean pip-update
