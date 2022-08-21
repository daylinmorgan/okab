.PHONY: build
build: dist/altair_saver_resvg-0.1a0-py3-none-linux_x86_64.whl

dist/altair_saver_resvg-0.1a0-py3-none-linux_x86_64.whl: altair_saver_resvg/src/vega-resvg
	python setup.py bdist_wheel -p linux-x86_64

altair_saver_resvg/src/vega-resvg: js/index.js
	$(MAKE) -C js build
	rm -f altair_saver_resvg/src/*
	cp js/vega-resvg altair_saver_resvg/src/vega-resvg


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
