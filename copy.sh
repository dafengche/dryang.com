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
cp ./services/celery_config.py.$flag ./services/celery_config.py
cp ./services/celery_worker_config.py.$flag ./services/celery_worker_config.py

echo "Failes copied"
