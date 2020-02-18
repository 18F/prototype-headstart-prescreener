serve-local:
	python app.py

deploy:
	cf push

serve:
	# (TODO) Productionize.
	python app.py
