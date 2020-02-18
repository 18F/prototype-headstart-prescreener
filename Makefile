serve-local:
	python app.py

deploy:
	cf push

deps:
	pip3 install --upgrade pip twine wheel

install: deps
	pip install --editable .[dev] --upgrade

serve:
	# (TODO) Productionize.
	python app.py
