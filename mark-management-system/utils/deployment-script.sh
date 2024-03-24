git pull

POSTGRES_USER_MMS=REDACTED
POSTGRES_PASSWORD_MMS=REDACTED
POSTGRES_DB_MMS=REDACTED
MMS_DATABASE_URL_DOCKER=REDACTED
SECRET_KEY_MMS=REDACTED
REFRESH_SECRET_KEY_MMS=REDACTED

docker-compose -f docker-compose.yml down --remove-orphans
docker volume rm mark-management-system_frontend-volume
docker rm -f $(docker ps -a -q)
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
docker image prune -a -f
