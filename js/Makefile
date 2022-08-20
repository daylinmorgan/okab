.PHONY: build
build:
	pkg index.js --no-bytecode --public-packages "*" --public -C GZip --target linux -o vega-resvg


.PHONY: build-all
build-all:
	pkg index.js --no-bytecode --public-packages "*" --public -C GZip --out-path dist/
