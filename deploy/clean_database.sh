#!/usr/bin/env bash

sudo supervisorctl stop all

psql -d postgres://miracle_asic:miracle_asic@localhost/miracle_asic_production -a -f /home/miracle_asic/miracle_asic/deploy/clean_database.sql

sudo supervisorctl start all