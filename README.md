Quick Start (Backend)

1) Prepare env files

```
cp env/backend.env.example env/backend.env.dev
# then edit env/backend.env.dev and fill in real values
```

2) Start services (dev)

```
make dev
```

⸻

Production Phase

```
cp env/backend.env.example env/backend.env.pro
# then edit env/backend.env.pro and fill in real values

# run production server
make pro
```
