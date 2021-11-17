# Dockerconfig
DOCKER_CMD=podman

IMAGE_BASE_NAME=spack-rhel8
IMAGE_VERSION=$(shell date +%Y%m%d)
REPO=ghcr.io/arcaneframework

.phony: build push

.DEFAULT_GOAL := build

build:
	${DOCKER_CMD} build -t ${REPO}/${IMAGE_BASE_NAME}:${IMAGE_VERSION} .. -f rhel8.dockerfile

push: build
	${DOCKER_CMD} push  ${REPO}/${IMAGE_BASE_NAME}:${IMAGE_VERSION}
