dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
pro:
	docker-compose -f docker-compose.yml -f docker-compose.pro.yml up -d --build
staging:
	docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d --build
traefik:
	docker-compose -f docker-compose.traefik.yml up -d
devdown:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
prodown:
	docker-compose -f docker-compose.yml -f docker-compose.pro.yml down
stagingdown:
	docker-compose -f docker-compose.yml -f docker-compose.staging.yml down
traefikdown:
	docker-compose -f docker-compose.traefik.yml down
devdownv:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v
prodownv:
	docker-compose -f docker-compose.yml -f docker-compose.pro.yml down -v
stagingownv:
	docker-compose -f docker-compose.yml -f docker-compose.staging.yml down -v
devwebbash:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec backend bash
prowebbash:
	docker-compose -f docker-compose.yml -f docker-compose.pro.yml exec backend bash
stagingwebbash:
	docker-compose -f docker-compose.yml -f docker-compose.staging.yml exec backend bash
probackendlog:
	docker compose -f docker-compose.yml -f docker-compose.pro.yml logs backend
profrontendlog:
	docker compose -f docker-compose.yml -f docker-compose.pro.yml logs frontend
stagingbackendlog:
	docker compose -f docker-compose.yml -f docker-compose.staging.yml logs backend
stagingfrontendlog:
	docker compose -f docker-compose.yml -f docker-compose.staging.yml logs frontend