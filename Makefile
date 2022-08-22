PLATFORMS = linux_x86_64 macosx_10_14_x86_64 win_amd64
VERSION = $(shell grep __version__ okab/__init__.py | awk -F'"' '{print $$2}')
WHEELS = $(addprefix dist/okab-${VERSION}-py3-none-,$(addsuffix .whl,$(PLATFORMS)))

.PHONY: wheels
wheels: $(WHEELS)

dist/okab-${VERSION}-py3-none-%.whl:
	@echo "==> Building $* Wheel <=="
	@rm -f okab/vega/*
	@$(MAKE) -C js dist/vega-resvg-$*
	@cp js/dist/vega-resvg-$* okab/vega/vega-resvg
	@python setup.py bdist_wheel -p $*

okab/vega/vega-resvg: js/index.js
	$(MAKE) -C js build
	rm -f okab/vega/*
	cp js/vega-resvg okab/vega/vega-resvg

.PHONY: examples
examples:
	rm -rf ./examples/*.{svg,png}
	cd examples && python make-examples.py

.PHONY: lint
lint:
	black .
	flake8 .
	mypy .

.PHONY:clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf js/vega-resvg
