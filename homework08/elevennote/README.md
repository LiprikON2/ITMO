# Note taking web app
> Built with docker and django

![tuwKfpn.png](https://i.imgur.com/tuwKfpn.png)

## Features

- Note tagging
    - [django-taggit](https://django-taggit.readthedocs.io/en/latest/getting_started.html)
    - [Bootstrap Tags Input](https://bootstrap-tagsinput.github.io/bootstrap-tagsinput/examples/)
- REST API

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
SECRET_KEY=IM_SECRET_50_CHAR_DJANGO_KEY
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
EMAIL_HOST_USER=YOUR_EMAIL
EMAIL_HOST_KEY=YOUR_PASSWORD
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

## REST API

### Getting token

Token will be in response to request at `/api/jwt-auth/`:
```json
{
    "email": "example@mail.com",
    "password": "secret"
}
```
then, in following request headers: `Authorization: JWT 123SUPERTOKEN`

