#!/bin/sh

for var in $(env | grep '^FLASK' | cut -d= -f1); do
    unset $var
done

for var in $(env | grep '^MSSQL' | cut -d= -f1); do
    unset $var
done