NAME=mathscinet
PLUGIN_NAME="Mathscinet"

SRC=src
ZIP=$(NAME).zip

SRC_FILES=$(wildcard $(SRC)/*)

$(ZIP): $(SRC_FILES)
	cd $(SRC); zip -r $(ZIP) *
	mv $(SRC)/$(ZIP) $(ZIP)

.PHONY: clean zip install test

clean:
	rm -f *.zip 

zip: $(ZIP)

install: $(ZIP)
	calibre-customize --a $(ZIP)

uninstall:
	calibre-customize --r $(PLUGIN_NAME)

test: 
	calibre-debug -e $(SRC)/test.py
