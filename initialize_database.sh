#!/bin/bash

MYSQL="/Applications/MAMP/Library/bin/mysql"
USER="root"
PASSWORD="root"

$MYSQL -u $USER -p$PASSWORD < ./database/db_version_1/drop_database.sql
$MYSQL -u $USER -p$PASSWORD < ./database/db_version_1/create_database.sql
$MYSQL -u $USER -p$PASSWORD < ./database/db_version_1/create_tables.sql
$MYSQL -u $USER -p$PASSWORD < ./database/db_version_1/create_user.sql
$MYSQL -u $USER -p$PASSWORD < ./database/db_version_1/insert_test_data.sql

echo "Database initialized successfully!"
