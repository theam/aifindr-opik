# Build stage
FROM node:20.15.0-alpine3.20 as builder

WORKDIR /opt/frontend

COPY package*.json ./
COPY patches ./patches
RUN npm install

# Copy and build the application
COPY . .

ARG OPIK_VERSION
ARG AUTH_DOMAIN
ARG AUTH_CLIENT_ID
ARG AUTH_AUDIENCE
ARG AIFINDR_API_URL

ENV VITE_APP_VERSION=${OPIK_VERSION}
ENV VITE_AUTH_DOMAIN=${AUTH_DOMAIN}
ENV VITE_AUTH_CLIENT_ID=${AUTH_CLIENT_ID}
ENV VITE_AUTH_AUDIENCE=${AUTH_AUDIENCE}
ENV VITE_PLUGINS_SCOPE=aifindr
ENV VITE_AIFINDR_API_URL=${AIFINDR_API_URL}

ENV NODE_OPTIONS="--max-old-space-size=8192"

ARG BUILD_MODE=production
RUN npm run build -- --mode $BUILD_MODE

# Production stage
FROM nginx:1.27.3-alpine3.20

# Copy the built files from the builder stage
COPY --from=builder /opt/frontend/dist /usr/share/nginx/html

RUN sed -i '/access_log.*main/d' /etc/nginx/nginx.conf

EXPOSE 5173

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
