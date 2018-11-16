echo off
title My Test batch file
:: see the title at the top
set FLASK_APP=run
set FLASK_DEV=development
set FLASK_DEBUG=1
start pipenv run flask run
exit