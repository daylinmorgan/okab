CMD := node ../index.js --spec ./example.vl.json --opts '{"mode":"vega-lite","scale":1}'

.PHONY: all
all: svg png vega

.PHONY: svg
svg:
	$(CMD) --format $@ --output example.svg

.PHONY: png
png:
	$(CMD) --format $@ --output example.png

.PHONY: vega
vega:
	$(CMD) --format $@ --output example.json

.PHONY: clean
clean:
	rm example.{png,svg,json}
