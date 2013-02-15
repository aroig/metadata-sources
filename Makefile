
PLUGINS=arxiv mathscinet zentralblatt

.PHONY: clean install all test

clean:
	for plg in $(PLUGINS); do cd $$plg; make clean; cd ..; done

all:
	for plg in $(PLUGINS); do cd $$plg; make zip; cd ..;done

install:
	for plg in $(PLUGINS); do cd $$plg; make install; cd ..; done

uninstall:
	for plg in $(PLUGINS); do cd $$plg; make uninstall; cd ..; done

test:
	for plg in $(PLUGINS); do cd $$plg; make test; cd ..; done

run:
	calibre-debug -g

kill:
	calibre -s

