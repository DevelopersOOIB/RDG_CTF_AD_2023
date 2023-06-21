#!/bin/sh

echo "Waiting for postgres..."
while ! python3 -c "import socket;import sys; sys.exit(0) if 0 == socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('postgres', 5432)) else sys.exit(1)"; do
  sleep 0.1
done
echo "PostgreSQL started"

bash /app/wait-for-it.sh -h custom-es -p 9200 -t 150 -- echo "Elasticsearch is started"

flask db upgrade
exec flask run --host 0.0.0.0