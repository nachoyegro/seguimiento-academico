#!/usr/bin/env bash


echo 'Borrando BD'
rm db.sqlite3

echo 'Corriendo las migraciones'
./manage.py migrate

echo 'Importando todo'
./manage.py importar
