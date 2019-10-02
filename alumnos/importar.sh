#!/usr/bin/env bash


echo 'Borrando BD'
rm db.sqlite3

echo 'Borrando migraciones viejas'
rm -rf core/migrations/

echo 'Creando migraciones'
./manage.py makemigrations core

echo 'Corriendo las migraciones'
./manage.py migrate

echo 'Importando todo'
./manage.py importar
