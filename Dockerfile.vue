# Dockerfile for Vue Frontend
FROM node:18-slim AS build

WORKDIR /app

# Copy package.json and install dependencies
COPY vue-dome/package*.json ./
RUN npm install

# Copy the rest of the application
COPY vue-dome/ .

# Build the application
RUN npm run build

# Serve with Nginx
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
