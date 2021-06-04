#!/bin/bash

VENV="venv"

PYTHON="/usr/bin/env python3"

if [[ ! -d $VENV ]] ; then
	$PYTHON -m venv $VENV
	source $VENV/bin/activate
	env GIT_SSL_NO_VERIFY=true $PYTHON -m pip install --upgrade -r python-requirements.txt
	deactivate
fi


