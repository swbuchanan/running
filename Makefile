.PHONY: serve serve-app register

serve:
	ngrok http 5000

serve-app:
	python listenerapp.py

register:
	python register_webhook.py
