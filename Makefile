.PHONY: all clean serve

all:
	@echo "Generating site"
	hugo --gc --minify

clean:
	@echo "Cleaning up"
	rm -rf ./public

serve:
	@echo "Start in server mode"
	hugo server --renderToMemory
