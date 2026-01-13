Quick Start (Backend)

1) Prepare env files

```
cp env/backend.env.example env/backend.env.dev
# then edit env/backend.dev.env and fill in real values
```

2) Start services (dev)

```
make dev
```

3) Run migrations

```
# run this to open backend terminal first
make webbash

python manage.py makemigrations
python manage.py migrate
```

⸻

Production

```
# create env/backend.prod.env (do NOT commit)
make pro
```
