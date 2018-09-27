CWD=$(shell pwd)
SRC_DIR=keepsake

.PHONY: all clean build lint tests install

all: clean lint launch

build: lint tests
	cd /tmp && virtualenv $(SRC_DIR) && cd $(SRC_DIR)
	cp -R $(CWD) /tmp/$(SRC_DIR)
	ls -l

clean:
	find . -regextype posix-extended -regex ".*.pyc" -type f -delete
	rm -rf /tmp/$(SRC_DIR) 2> /dev/null

release: build
	cd /tmp/$(SRC_DIR)/$(SRC_DIR) && python setup.py sdist
	ls -l

lint:
	flake8 $(SRC_DIR)

tests:
	python -m unittest discover -v tests

install: tests lint
	python setup.py install
	unlocker init
	unlocker install 2> /dev/null
	keepsake fix
	cp Desktop /usr/share/applications/$(SRC_DIR).desktop

launch: tests
	python $(SRC_DIR).py
