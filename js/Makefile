PLATFORMS = manylinux_2_17_x86_64 macosx_10_14_x86_64 win_amd64
BINARIES := $(addprefix dist/okab-,$(PLATFORMS))
PKG = pkg . --no-bytecode --public-packages "*" --public --no-native-build -C GZip
#-C GZip

.PHONY: all
all: $(BINARIES)

.PHONY: lint
lint:
	prettier -w .

dist/okab-manylinux_2_17_x86_64:
	./scripts/get-node-addon linux-x64-gnu
	$(PKG) -t node18-linux-x64 -o $@

dist/okab-macosx_10_14_x86_64:
	./scripts/get-node-addon darwin-x64
	$(PKG) -t node18-macos-x64 -o $@

dist/okab-win_amd64:
	./scripts/get-node-addon win32-x64-msvc
	$(PKG) -t node18-win-x64 -o $@
	mv $@.exe $@

.PHONY: clean
clean:
	rm -rf dist/
	rm -r node_modules/@resvg/resvg-js-*
