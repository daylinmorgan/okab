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

# .PHONY: all

# all: example.png example.svg example.json

# example.%:
# 	node ../index.js ./example.vl.json '{"mode":"vega-lite","scale":1}' $* $@

# example.json:
# 	node ../index.js ./example.vl.json '{"mode":"vega-lite","scale":1}' 'vega' ./example.json

# .PHONY: clean
# clean:
# 	rm example.png example.svg example.json
