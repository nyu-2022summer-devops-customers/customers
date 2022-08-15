# These can be overidden with env vars.
REGISTRY ?= us.icr.io
NAMESPACE ?= devops_customers
IMAGE_NAME ?= customers
IMAGE_TAG ?= 1.0
IMAGE ?= $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)
# PLATFORM ?= "linux/amd64,linux/arm64"
PLATFORM ?= "linux/amd64"
CLUSTER ?= devops-customers

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-\\.]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: all
all: help

.PHONY: clean
clean:	## Removes all dangling build cache
	$(info Removing all dangling build cache..)
	-docker rmi $(IMAGE)
	docker image prune -f
	docker buildx prune -f

.PHONY: venv
venv: ## Create a Python virtual environment
	$(info Creating Python 3 virtual environment...)
	python3 -m venv .venv

.PHONY: install
install: ## Install dependencies
	$(info Installing dependencies...)
	sudo pip install -r requirements.txt

.PHONY: lint
lint: ## Run the linter
	$(info Running linting...)
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
	pylint service

.PHONY: test
test: ## Run the unit tests
	$(info Running tests...)
	nosetests --with-spec --spec-color

.PHONY: run
run: ## Run the service
	$(info Starting service...)
	honcho start

.PHONY: deploy
deploy: ## Deploy the service on local Kubernetes
	$(info Deploying service locally...)
	kubectl -n default apply -f deploy/

.PHONY: undeploy
undeploy: ## Deploy the service on local Kubernetes
	$(info Deploying service locally...)
	kubectl delete pods,services,replicasets,deployments,statefulsets --all -n default

.PHONY: team-login
team-login: ## Login the IBM Cloud
	$(info Login the IBM Cloud cluster $(CLUSTER)...)
	ibmcloud login -a cloud.ibm.com -g Default -r us-south --apikey @~/apikey-team.json
	ibmcloud cr login
	ibmcloud ks cluster config --cluster $(CLUSTER)
	kubectl cluster-info

.PHONY: dev-deploy
dev-deploy:
	$(info Deploy to dev ns)
	kubectl -n dev apply -f deploy/dev/

.PHONY: prod-deploy
prod-deploy:
	$(info Deploy to prod ns)
	kubectl -n prod apply -f deploy/prod/

.PHONY: dev-undeploy
dev-undeploy:
	$(info Delete all in dev ns)
	kubectl delete pods,services,replicasets,deployments,statefulsets --all -n dev


.PHONY: prod-undeploy
prod-undeploy:
	$(info Delete all in prod ns)
	kubectl delete pods,services,replicasets,deployments,statefulsets --all -n prod



############################################################
# COMMANDS FOR BUILDING THE IMAGE
############################################################

.PHONY: init
init: export DOCKER_BUILDKIT=1
init:	## Creates the buildx instance
	$(info Initializing Builder...)
	docker buildx create --use --name=qemu
	docker buildx inspect --bootstrap

.PHONY: build
build:	## Build all of the project Docker images
	$(info Building $(IMAGE) for $(PLATFORM)...)
	docker buildx build --file Dockerfile  --pull --platform=$(PLATFORM) --tag $(IMAGE) --load .

.PHONY: remove
remove:	## Stop and remove the buildx builder
	$(info Stopping and removing the builder image...)
	docker buildx stop
	docker buildx rm

.PHONY: push
push:
	docker push us.icr.io/devops_customers/customers:1.0
