FONT_RELEASE = https://github.com/liberationfonts/liberation-fonts/files/7261482/liberation-fonts-ttf-2.1.5.tar.gz
PLATFORMS = manylinux_2_17_x86_64 macosx_10_14_x86_64 win_amd64
#VERSION := $(shell grep __version__ okab/_version.py | awk -F'"' '{print $$2}')
VERSION := $(shell python -m setuptools_scm)
WHEELBASE := dist/okab-$(VERSION)-py3-none-
WHEELS := $(foreach platform,$(PLATFORMS), $(WHEELBASE)$(platform).whl)
TARGET ?= manylinux_2_17_x86_64

.PHONY: wheels
## generate all of the wheels
wheels: $(WHEELS)
	@rm okab/bin/okab


.PHONY: install
## install the package in the local venv
install: okab/bin/okab
	source ./venv/bin/activate; \
		pip install -e .

.PHONY: bootstrap
## bootstrap the project/dev environemnt
bootstrap: venv npm fonts

.PHONY: venv
venv:
	python -m venv venv
	source ./venv/bin/activate; \
		pip install -e ".[dev]"

.PHONY: npm
npm:
	npm install --prefix js/

.PHONY: single-wheel
single-wheel: $(WHEELBASE)$(TARGET).whl

$(WHEELBASE)%.whl:
	@echo "==> Building $* Wheel <=="
	@rm -f okab/bin/okab
	@rm -rf build
	$(MAKE) -C js dist/okab-$*
	@cp js/dist/okab-$* okab/bin/okab
	@python setup.py bdist_wheel -p $*

okab/bin/okab:
	$(MAKE) -C js dist/okab-$(TARGET)
	rm -f okab/bin/okab
	cp js/dist/okab-$(TARGET) okab/bin/okab

.PHONY: fonts
## download liberation sans
fonts: okab/bin/fonts

okab/bin/fonts:
	mkdir okab/bin/fonts -p
	wget -O okab/bin/fonts/liberation.tar.gz $(FONT_RELEASE)
	tar -xvf okab/bin/fonts/liberation.tar.gz --directory=okab/bin/fonts
	rm okab/bin/fonts/liberation.tar.gz

.PHONY: examples
## regenerate example charts
examples:
	rm -rf ./examples/*.{svg,png}
	cd examples && python make-examples.py

.PHONY: lint
## run formatting, linting, and typechecks
lint:
	isort okab/
	black okab/
	flake8 okab/
	mypy okab/

.PHONY:clean
## clean build outputs
clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf js/okab

.PHONY: deep-clean
deep-clean:
	rm -rf okab/bin/{fonts,okab}
	rm -rf js/dist
	rm -rf venv

.PHONY: help
help: ## try `make help`
	@awk '/^[a-z.A-Z_-]+:/ { helpMessage = match(lastLine, /^##(.*)/); \
		if (helpMessage) { helpCommand = substr($$1, 0, index($$1, ":")-1); \
		helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
		printf "\033[36m%-9s\033[0m - %s\n", \
		helpCommand, helpMessage;}} { lastLine = $$0 }' $(MAKEFILE_LIST)
