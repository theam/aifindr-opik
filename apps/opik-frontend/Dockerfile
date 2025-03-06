# Build stage
FROM node:20.15.0-alpine3.20 as builder

WORKDIR /opt/frontend

COPY package*.json ./
COPY patches ./patches
RUN npm install

# Copy and build the application
COPY . .

ARG OPIK_VERSION

ENV VITE_APP_VERSION=${OPIK_VERSION}
ENV VITE_PLUGINS_SCOPE=aifindr

ENV NODE_OPTIONS="--max-old-space-size=8192"

ARG BUILD_MODE=production
RUN npm run build -- --mode $BUILD_MODE

# Production stage
FROM nginx:1.27.3-alpine3.20

# Copy the built files from the builder stage
COPY --from=builder /opt/frontend/dist /usr/share/nginx/html

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

RUN sed -i '/access_log.*main/d' /etc/nginx/nginx.conf

EXPOSE 5173

# Start Nginx
ENTRYPOINT ["/docker-entrypoint.sh"]
