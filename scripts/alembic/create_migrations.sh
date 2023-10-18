#read -p "Enter name of migration: " message
export BOT_CONTAINER_NAME=XpymXpymBot
docker exec ${BOT_CONTAINER_NAME} alembic -c /usr/src/app/XpymXpymBot/scripts/alembic/alembic.ini revision --autogenerate -m "xpymxpymbot"