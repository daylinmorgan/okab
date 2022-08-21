PLATFORMS = linux_x86_64 macosx_10_14_x86_64 win_amd64
VERSION = $(shell grep __version__ altair_saver_resvg/__init__.py | awk -F'"' '{print $$2}')
WHEELS = $(addprefix dist/altair_saver_resvg-${VERSION}-py3-none-,$(addsuffix .whl,$(PLATFORMS)))

.PHONY: wheels
wheels: $(WHEELS)

dist/altair_saver_resvg-${VERSION}-py3-none-%.whl:
	@echo "==> Building $* Wheel <=="
	@rm -f altair_saver_resvg/src/*
	@$(MAKE) -C js dist/vega-resvg-$*
	@cp js/dist/vega-resvg-$* altair_saver_resvg/src/vega-resvg
	@python setup.py bdist_wheel -p $*

altair_saver_resvg/src/vega-resvg: js/index.js
	$(MAKE) -C js build
	rm -f altair_saver_resvg/src/*
	cp js/vega-resvg altair_saver_resvg/src/vega-resvg

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
