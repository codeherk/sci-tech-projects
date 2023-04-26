full-start: start-backend start-frontend

start-backend:
	docker compose -f backend/docker-compose.yml down
	docker compose -f backend/docker-compose.yml up --build -d 

start-frontend:
	npm start --prefix frontend/microsatellite