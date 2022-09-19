FONT_RELEASE = https://github.com/liberationfonts/liberation-fonts/files/7261482/liberation-fonts-ttf-2.1.5.tar.gz
PLATFORMS = manylinux_2_17_x86_64 macosx_10_14_x86_64 win_amd64
VERSION := $(shell python -m setuptools_scm)
WHEELBASE := dist/okab-$(VERSION)-py3-none-
WHEELS := $(foreach platform,$(PLATFORMS), $(WHEELBASE)$(platform).whl)
TARGET ?= manylinux_2_17_x86_64

## lint | run formatting, linting, and typechecks
.PHONY: lint
lint:
	isort okab/
	black okab/
	flake8 okab/
	mypy okab/

## wheels | generate all of the wheels
.PHONY: wheels
wheels: version-js $(WHEELS)
	@rm -f okab/bin/okab

## install | install the package in the local venv
.PHONY: install
install: okab/bin/okab
	source ./venv/bin/activate; \
		pip install -e .

## bootstrap | bootstrap the project/dev environemnt
.PHONY: bootstrap
bootstrap: venv npm fonts

.PHONY: venv
venv:
	python -m venv venv
	source ./venv/bin/activate; \
		pip install -e ".[dev]"

.PHONY: npm
npm:
	npm install --prefix js/

## single-wheel | build wheel for TARGET
.PHONY: single-wheel
single-wheel: version-js $(WHEELBASE)$(TARGET).whl

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

.PHONY: version-js
version-js:
	@echo '{"version":"$(VERSION)"}' > js/src/version.json

## fonts | download liberation sans
.PHONY: fonts
fonts: okab/bin/fonts

okab/bin/fonts:
	mkdir okab/bin/fonts -p
	wget -O okab/bin/fonts/liberation.tar.gz $(FONT_RELEASE)
	tar -xvf okab/bin/fonts/liberation.tar.gz --directory=okab/bin/fonts
	rm okab/bin/fonts/liberation.tar.gz

## examples | regenerate example charts
.PHONY: examples
examples:
	rm -rf ./examples/*.{svg,png}
	cd examples && python make-examples.py

## clean | remove build outputs
.PHONY:clean
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

-include .task.mk
USAGE = ==> {a.b_green}Okab Development Tasks{a.end} <==\n\n{a.header}usage{a.end}:\n  make <recipe>\n
$(if $(wildcard .task.mk),,.task.mk: ; curl -fsSL https://raw.githubusercontent.com/daylinmorgan/task.mk/v22.9.19/task.mk -o .task.mk)
