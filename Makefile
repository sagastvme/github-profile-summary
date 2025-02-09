APP_NAME = github_summary

run:
	docker run -p 5000:5000  $(APP_NAME)

build:
	docker build -t $(APP_NAME) .
