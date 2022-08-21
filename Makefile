.PHONY: build
build: dist/altair_saver_resvg-0.1a1-py3-none-linux_x86_64.whl

.PHONY: wheels
wheels: $(addprefix dist/altair_saver_resvg-0.1a1-py3-none-,$(addsuffix .whl,linux_x86_64 macosx_10_14_x86_64 win_amd64))

dist/altair_saver_resvg-0.1a1-py3-none-linux_x86_64.whl: ./js/dist/vega-resvg-linux-x64
	@echo "==> Building Linux Wheel <=="
	@rm -f altair_saver_resvg/src/*
	@cp $< altair_saver_resvg/src/vega-resvg
	@python setup.py bdist_wheel -p linux_x86_64

dist/altair_saver_resvg-0.1a1-py3-none-macosx_10_14_x86_64.whl: ./js/dist/vega-resvg-macos-x64
	@echo "==> Building MacOS x64 Wheel <=="
	@rm -f altair_saver_resvg/src/*
	@cp ./js/dist/vega-resvg-macos-x64 altair_saver_resvg/src/vega-resvg
	@python setup.py bdist_wheel -p macosx_10_14_x86_64

dist/altair_saver_resvg-0.1a1-py3-none-win_amd64.whl: ./js/dist/vega-resvg-win-x64.exe
	@echo "==> Building Windows Wheel <=="
	@rm -f altair_saver_resvg/src/*
	@cp ./js/dist/vega-resvg-win-x64.exe altair_saver_resvg/src/vega-resvg
	@python setup.py bdist_wheel -p win_amd64

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
