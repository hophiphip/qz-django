# QZ Django

## Quick start
```sh
docker-compose up -d
```

## After starting tha app run tests
```sh
docker-compose exec web python manage.py test
```

## Check code-style
```sh
docker-compose exec web pycodestyle .
```