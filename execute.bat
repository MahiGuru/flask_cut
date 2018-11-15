echo off
title My Test batch file
:: see the title at the top
set FLASK_APP=thetopcut
set FLASK_DEV=development
start pipenv run flask run
exit