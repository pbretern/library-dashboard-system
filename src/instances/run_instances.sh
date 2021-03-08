#!/bin/sh
# the absolute path
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
# calling the python scripts to import the data

PYTHONPATH="${PYTHONPATH}:/usr/src/app"
 
"$SCRIPTPATH/budget_import.py"
"$SCRIPTPATH/umsatz_import.py"
"$SCRIPTPATH/loan_import.py"
"$SCRIPTPATH/newacq_import.py"
"$SCRIPTPATH/readingroom.py"
