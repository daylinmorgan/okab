FONT_RELEASE = https://github.com/liberationfonts/liberation-fonts/files/7261482/liberation-fonts-ttf-2.1.5.tar.gz
PLATFORMS = manylinux_2_17_x86_64 macosx_10_14_x86_64 win_amd64
#VERSION := $(shell grep __version__ okab/_version.py | awk -F'"' '{print $$2}')
VERSION := $(shell python -m setuptools_scm)
WHEELBASE := dist/okab-$(VERSION)-py3-none-
WHEELS = $(addprefix $(WHEELBASE),$(addsuffix .whl,$(PLATFORMS)))
TARGET ?= manylinux_2_17_x86_64

.PHONY: wheels
## generate all of the wheels
wheels: $(WHEELS)

.PHONY: linux-wheel
linux-wheel: $(WHEELBASE)manylinux_2_17_x86_64.whl

$(WHEELBASE)%.whl:
	@echo "==> Building $* Wheel <=="
	@rm -f okab/vega/vega-resvg
	@rm -rf build
	$(MAKE) -C js dist/vega-resvg-$*
	@cp js/dist/vega-resvg-$* okab/vega/vega-resvg
	@python setup.py bdist_wheel -p $*

okab/vega/vega-resvg: js/index.js
	$(MAKE) -C js dist/vega-resvg-$(TARGET)
	rm -f okab/vega/vega-resvg
	cp js/dist/vega-resvg-$(TARGET) okab/vega/vega-resvg

.PHONY: fonts
## download liberation sans
fonts:
	mkdir okab/vega/fonts -p
	wget -O okab/vega/fonts/liberation.tar.gz $(FONT_RELEASE)
	tar -xvf okab/vega/fonts/liberation.tar.gz --directory=okab/vega/fonts
	rm okab/vega/fonts/liberation.tar.gz

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
	rm -rf js/vega-resvg


.PHONY: help
help: ## try `make help`
	@awk '/^[a-z.A-Z_-]+:/ { helpMessage = match(lastLine, /^##(.*)/); \
		if (helpMessage) { helpCommand = substr($$1, 0, index($$1, ":")-1); \
		helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
		printf "\033[36m%-9s\033[0m - %s\n", \
		helpCommand, helpMessage;}} { lastLine = $$0 }' $(MAKEFILE_LIST)
