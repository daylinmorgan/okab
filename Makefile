.PHONY: build
build: dist/altair_saver_resvg-0.1.0-py3-none-any.whl

dist/altair_saver_resvg-0.1.0-py3-none-any.whl: altair_saver_resvg/src/vega-resvg
	python -m build --wheel

altair_saver_resvg/src/vega-resvg: js/index.js
	$(MAKE) -C js build
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
