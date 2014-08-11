ifndef PLUGINS_DIR
PLUGINS_DIR := /usr/local/nagios/libexec
$(info PLUGINS_DIR not set, using ${PLUGINS_DIR} as a default.)
endif

CHECKS=$(wildcard checks/check*)

install:
	@for f in ${CHECKS}; do \
		[ ! -e "${PLUGINS_DIR}/`basename $$f`" ] && sudo ln -s $$f ${PLUGINS_DIR}/`basename $$f`; \
	done

.PHONY: install
