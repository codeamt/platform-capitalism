SHELL := /bin/bash
SERVICE = platform-simulation
REGION = us-east-1
IMAGE = $(SERVICE):latest
LS_IMAGE = $(SERVICE):lightsail

build:
	docker build -t $(IMAGE) .
	docker tag $(IMAGE) $(LS_IMAGE)

push:
	aws lightsail push-container-image --service-name $(SERVICE) --label app --image $(LS_IMAGE) --region $(REGION)

deploy:
	aws lightsail create-container-service-deployment \
		--service-name $(SERVICE) \
		--containers file://infra/lightsail/lightsail.yaml \
		--public-endpoint '{"containerName":"app","containerPort":8080}' \
		--region $(REGION)

logs:
	aws lightsail get-container-log --service-name $(SERVICE) --region $(REGION)

run-local:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
