#!/bin/sh
pycodestyle webauto/
pydocstyle webauto/
pylint webauto/
pyflakes webauto/
