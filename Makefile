
IMAGE = natasha-demo
REGISTRY = cr.yandex/crpivkgjcn1eim67enme

test:
	flake8 --extend-ignore=E501,W503 app.py test.py
	pytest -vv test.py

image:
	docker build -t $(IMAGE) .

push:
	docker tag $(IMAGE) $(REGISTRY)/$(IMAGE)
	docker push $(REGISTRY)/$(IMAGE)

deploy:
	yc serverless container revision deploy \
		--container-name default \
		--image $(REGISTRY)/$(IMAGE):latest \
		--cores 1 \
		--memory 512MB \
		--concurrency 2 \
		--execution-timeout 30s \
		--folder-name natasha-demo
