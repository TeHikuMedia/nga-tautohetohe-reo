DOCKER_REGISTRY := 473856431958.dkr.ecr.ap-southeast-2.amazonaws.com
IMAGE_NAME := $(shell basename `git rev-parse --show-toplevel` | tr '[:upper:]' '[:lower:]')
IMAGE := $(DOCKER_REGISTRY)/$(IMAGE_NAME)
HAS_DOCKER ?= $(shell which docker)
RUN ?= $(if $(HAS_DOCKER), docker run $(DOCKER_ARGS) --rm -v $$(pwd):/work -w /work -u $(UID):$(GID) $(IMAGE))
UID ?= $(shell id -u)
GID ?= $(shell id -g)
DOCKER_ARGS ?= 
GIT_TAG ?= $(shell git log --oneline | head -n1 | awk '{print $$1}')
LOG_LEVEL ?= DEBUG

.PHONY: corpus docker docker-push docker-pull enter enter-root4

corpus: corpus/hansard-reo-māori.txt

corpus/hansard-reo-māori.txt: scripts/import_nga_tautohetohe.py hansardreomāori.csv
	$(RUN) python3 $< --csv-file $(word 2,$^) --text-file $@ --log-level $(LOG_LEVEL)

PROFILE ?= default
docker-login:
	eval $$(aws ecr get-login --no-include-email --profile $(PROFILE) --region ap-southeast-2 | sed 's|https://||')

clean:
	rm -rf corpus/*

docker:
	docker build $(DOCKER_ARGS) --tag $(IMAGE):$(GIT_TAG) .
	docker tag $(IMAGE):$(GIT_TAG) $(IMAGE):latest

docker-push:
	docker push $(IMAGE):$(GIT_TAG)
	docker push $(IMAGE):latest

docker-pull:
	docker pull $(IMAGE):$(GIT_TAG)
	docker tag $(IMAGE):$(GIT_TAG) $(IMAGE):latest

enter: DOCKER_ARGS=-it
enter:
	$(RUN) bash

enter-root: DOCKER_ARGS=-it
enter-root: UID=root
enter-root: GID=root
enter-root:
	$(RUN) bash
