FONT_RELEASE = https://github.com/liberationfonts/liberation-fonts/files/7261482/liberation-fonts-ttf-2.1.5.tar.gz
PLATFORMS = manylinux_2_17_x86_64 macosx_10_14_x86_64 win_amd64
#VERSION := $(shell grep __version__ okab/_version.py | awk -F'"' '{print $$2}')
VERSION := $(shell python -m setuptools_scm)
WHEELBASE := dist/okab-$(VERSION)-py3-none-
WHEELS = $(addprefix $(WHEELBASE),$(addsuffix .whl,$(PLATFORMS)))

test:
	echo $(WHEELS)

.PHONY: wheels
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
	$(MAKE) -C js build
	rm -f okab/vega/vega-resvg
	cp js/vega-resvg okab/vega/vega-resvg

.PHONY: fonts
fonts:
	mkdir okab/vega/fonts -p
	wget -O okab/vega/fonts/liberation.tar.gz $(FONT_RELEASE)
	tar -xvf okab/vega/fonts/liberation.tar.gz --directory=okab/vega/fonts
	rm okab/vega/fonts/liberation.tar.gz

.PHONY: examples
examples:
	rm -rf ./examples/*.{svg,png}
	cd examples && python make-examples.py

.PHONY: lint
lint:
	isort .
	black .
	flake8 .
	mypy okab/

.PHONY:clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf js/vega-resvg
