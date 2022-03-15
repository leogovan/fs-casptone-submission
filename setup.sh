#!/bin/bash
#export DATABASE_URL="postgresql://127.0.0.1:5432/fs-capstone-submission"
export FLASK_APP=app.py
export AUTH0_DOMAIN='fsnd-leogovan.eu.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='casting-agency'
echo $DATABASE_URL
echo $FLASK_APP
echo $AUTH0_DOMAIN
echo $ALGORITHMS
echo $API_AUDIENCE
echo "setup.sh script executed successfully!"