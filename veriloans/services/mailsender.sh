#!/bin/sh
echo -e "Running Bakcup SH Service ! \n"

echo -e "Dumping postgres database under the pg_dump function ..."
PGPASSWORD='adminmodels' pg_dump -U postgres -h localhost sangabbb >> /var/www/html/veriloans/services/backup.sql

echo -e "\n Version of python: \n"
/var/www/html/veriloans/venv/bin/python -V

echo -e "\n Sending dumped sql file to recipient lists email ... \n"
/var/www/html/veriloans/venv/bin/python /var/www/html/veriloans/services/sendtomail.py



