# Subway KL
![UI Preview](/docs/sample.png)


## Development Docker Quick Start

You need to have Docker and Docker Compose. Git clone this project and enter its root directory, then run the following:
```bash
cp dev-env .env
docker-compose up

# Open a new terminal
docker exec -it [django container name] bash
./manage.py makemigrations
./manage.py migrate
```
You may need to run `docker-compose` with `sudo` if your user account does not have permission to use Docker directly.

---
### Do scraping
Access http://127.0.0.1:8000/scrape

### Do geocoding
Access http://127.0.0.1:8000/retrieve

### Access UI
Access http://127.0.0.1:8000

---
### To improve Question Answer ML
We can modify the context to improve the Question Answer ML.

To modify the data:
1. [Create superuser account](#create-superuser-account).
2. Access http://127.0.0.1:8000/admin
3. Login
4. Goto SubwayContext
5. Do edit there.

Be aware: SubwayContext is a singleton model.

---
### Create superuser account
```bash
docker exec -it [django container name] bash
./manage.py createsuperuser
```
##### Reference
- [Django create admin user](https://docs.djangoproject.com/en/5.0/intro/tutorial02/#creating-an-admin-user)

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
