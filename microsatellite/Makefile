install:
	[ -d "frontend/microsatellite/node_modules" ] || npm install --prefix frontend/microsatellite

full-start: start-backend start-frontend

stop-backend:
	docker compose -f backend/docker-compose.yml down
	
start-backend:
	docker compose -f backend/docker-compose.yml down
	docker compose -f backend/docker-compose.yml up --build -d 

start-frontend:
	npm start --prefix frontend/microsatellite
