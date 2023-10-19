#read -p "Enter name of migration: " message
export BOT_CONTAINER_NAME=XpymXpymBot
docker exec ${BOT_CONTAINER_NAME} "cd /usr/src/app/scripts/alembic/ && alembic revision --autogenerate -m 'xpymxpymbot'"