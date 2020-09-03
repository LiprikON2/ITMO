# Homework 08

### Running

1. Install [docker](https://docs.docker.com/get-docker/)
2. Install docker-compose:
```
pip install docker-compose
```
4. Create `settings.ini` in `elevennote/src/config/settings/`

`elevennote/src/config/settings/settings.ini`:
```ini
[settings]
SECRET_KEY='IM_SECRET_50_CHAR_DJANGO_KEY'
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
```

!!! attention Secret key
`%` symbols in `SECRET_KEY` needs to be doubled

!!!

6. Run commands:
```
docker-compose build
```

```
docker-compose up
```

7. Access server at [localhost:8000](http://localhost:8000/)