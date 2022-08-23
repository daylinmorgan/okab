PLATFORMS := linux_x86_64 macosx_10_14_x86_64 win_amd64

.PHONY: lint
lint:
	prettier -w .

.PHONY: build
build:
	pkg index.js --no-bytecode --public-packages "*" --public -C GZip --target linux -o vega-resvg


.PHONY: build-all
build-all:
	pkg index.js --no-bytecode --public-packages "*" --public -C GZip --out-path dist/


dist/vega-resvg-linux_x86_64:
	pkg . --no-bytecode --public-packages "*" --public -C GZip -t node18-linux-x64 -o $@

dist/vega-resvg-macosx_10_14_x86_64:
	pkg . --no-bytecode --public-packages "*" --public -C GZip -t node18-macos-x64 -o $@

dist/vega-resvg-win_amd64:
	pkg . --no-bytecode --public-packages "*" --public -C GZip -t node18-win-x64 -o $@
	mv $@.exe $@

.PHONY: clean
clean:
	rm -rf dist/
