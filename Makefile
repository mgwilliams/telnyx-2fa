.PHONY: test build push

test: build
	docker run -it --entrypoint ./run-tests.sh telnyx-2fa

build:
	docker build . -t telnyx-2fa
