#!/bin/sh

if [ "$#" -eq 0 ]; then
  echo "No argument, flag set to 'dev'"
  flag="dev"
else
  flag=$1
fi

if [ $flag != "dev" ] && [ $flag != "prod" ]; then
  echo "Supported flags: dev (default), prod"
  exit 1
fi

cp ./apps/settings.py.$flag ./apps/settings.py
cp ./services/celeryconfig.py.$flag ./services/celeryconfig.py
cp ./services/servicelib/cache.py.$flag ./services/servicelib/cache.py
cp ./services/servicelib/db.py.$flag ./services/servicelib/db.py

echo "Failes copied"
