# Django Server
## Development Docker Quick Start

You need to have Docker and Docker Compose. Git clone this project and enter its root directory, then run the following:
```bash
cp dev-env .env
docker-compose up

# Open a new terminal
docker exec -it [django container name] bash
pipenv run ./manage.py makemigrations
pipenv run ./manage.py migrate
```
You may need to run `docker-compose` with `sudo` if your user account does not have permission to use Docker directly.

---
## Pre-commit setup

1. Install pre-commit
```
sudo apt install pre-commit
```
2. Setup pre-commit in git repo
```
pre-commit install
```
3. Run pre-commit in all file (optional)
```
pre-commit run --all-files
```

##### Reference
- [Pre-commit Install](https://pre-commit.com/#install)

---
## Reference
