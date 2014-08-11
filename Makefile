ifndef PLUGINS_DIR
PLUGINS_DIR := /usr/local/nagios/libexec
$(info PLUGINS_DIR not set, using ${PLUGINS_DIR} as a default.)
endif

CHECKS=$(wildcard checks/check*)

# $(foreach f, $*.txt, printf "%s\n" 0a "$$(grep -o '[0-9]\+' $f | sed 's/.*/read \"&\"/')" "" . w q | ed $f)
install:
	@for f in ${CHECKS}; do \
		[ ! -e "${PLUGINS_DIR}/`basename $$f`" ] && echo ln -s $$f ${PLUGINS_DIR}/`basename $$f`; \
	done

.PHONY: install
