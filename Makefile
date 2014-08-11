ifndef PLUGINS_DIR
PLUGINS_DIR := /usr/local/nagios/libexec
$(info PLUGINS_DIR not set, using ${PLUGINS_DIR} as a default.)
endif

CHECKS:=$(wildcard checks/check*)
REQUIREMENTS_FILES:=$(wildcard checks/requirements*.txt)
CUR_DIR:=$(shell pwd)
CUR_DATE:=$(shell date +'%Y%m%d')

install: requirements
	@for f in ${CHECKS}; do \
		test -e "${PLUGINS_DIR}/`basename $$f`" || sudo ln -s ${CUR_DIR}/$$f ${PLUGINS_DIR}/`basename $$f`; \
	done

requirements:
	@cat ${REQUIREMENTS_FILES} | sort | uniq > ${CUR_DIR}/requirements-${CUR_DATE}.txt
	@sudo pip install -r ${CUR_DIR}/requirements-${CUR_DATE}.txt
	@-rm ${CUR_DIR}/requirements-${CUR_DATE}.txt

.PHONY: install
