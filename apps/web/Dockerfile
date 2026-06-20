# --- build stage: compile the frontend with Vite ---
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* .npmrc ./
RUN npm install
COPY . .
RUN npm run build

# --- runtime stage: nginx serves the static build + proxies the API ---
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
