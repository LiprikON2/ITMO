# Note taking web app
> Built with docker and django

## Running

1. Install [docker](https://docs.docker.com/get-docker/)
2. Install docker-compose:
```bash
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


> **:warning: Warning:** `%` symbols in `SECRET_KEY` needs to be doubled

6. Run commands:
```bash
docker-compose build
```

```bash
docker-compose up
```

7. Access server at [localhost:8000](http://localhost:8000/)


## Tests

### Run tests
```bash
docker-compose run web python manage.py test
```
### Check test coverage
```bash
docker-compose run web coverage run --source='.' manage.py test notes
```
```bash
docker-compose run web coverage report
```

## Creating admin user

1. Run the app:
```bash
docker-compose up
```
2. Access `dg01`'s bash

```bash
docker exec -it dg01 bash
```
3. Inside bash:
```bash
python manage.py createsuperuser
```

Or in one line:
```bash
docker-compose run web python manage.py createsuperuser
```