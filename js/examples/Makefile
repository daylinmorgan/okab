.PHONY: all
all: example.png example.svg example.json

example.%:
	node ../index.js ./example.vl.json '{"mode":"vega-lite","scale":1}' $* $@

example.json:
	node ../index.js ./example.vl.json '{"mode":"vega-lite","scale":1}' 'vega' ./example.json

.PHONY: clean
clean:
	rm example.png example.svg example.json
