
.DEFAULT_GOAL := help
SHELL := /bin/bash


REPO_DIR := $(abspath $(CURDIR)/..)

# NOTE that IMAGES variable can change when docker-compose.yml gets rebuilt. Do NOT use := !!!
IMAGES = $(shell ./bin/yq eval '.services.*.image' docker-compose.yml)

export DOCKER_REGISTRY ?= registry:5000


.PHONY: info
info: ## lists environments and required tools
	# tools
	@echo 'docker         : $(shell docker --version 2>/dev/null || echo ERROR required tool missing )'
	@echo 'docker compose : $(shell docker compose version 2>/dev/null || echo ERROR required tool missing )'
	@echo 'docker buildx  : $(shell docker buildx version 2>/dev/null || echo WARNING optional tool missing )'
	@echo 'make           : $(shell make --version 2>&1 | head -n 1)'
	@echo 'awk            : $(shell awk -W version 2>&1 | head -n 1)'
	@echo 'sed            : $(shell sed  --version 2>&1 | head -n 1)'
	# environments
	@echo "REPO_DIR        = ${REPO_DIR}"
	@echo "IMAGES          = ${IMAGES}"
	@echo "DOCKER_REGISTRY = ${DOCKER_REGISTRY}"


.PHONY: update-version
update-version:
	cd $(REPO_DIR) \
	&& . update_version.sh \
	&& cd -

.PHONY: compose
compose: update-version ## creates docker-compose.yml
	# creating compose specs
	cd $(REPO_DIR) \
	&& .osparc/bin/ooil compose -f .osparc/docker-compose.yml


.PHONY: build build-nc
build build-nc: compose ## builds image. Suffix -nc disables cache
	# building
	docker compose build $(if $(findstring -nc,$@),--no-cache,)


.PHONY: push
push: ## retags and pushes to ${DOCKER_REGISTRY}
	# tag & push
	@for image in ${IMAGES}; do \
		echo "Tagging and pushing ${DOCKER_REGISTRY}/$$image ..."; \
		docker tag "$$image" "${DOCKER_REGISTRY}/$$image"; \
		docker push "${DOCKER_REGISTRY}/$$image"; \
	done
	# registry view
	@curl --silent ${DOCKER_REGISTRY}/v2/_catalog | jq



.PHONY: all
all: compose build-nc push ## all workflow
	@echo "'${IMAGES}' built, and pushed to '${DOCKER_REGISTRY}'"


.PHONY: help
help: ## help on rule's targets
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
