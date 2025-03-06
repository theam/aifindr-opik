#!/bin/sh
set -e

APP_DIR=/usr/share/nginx/html

# Generate configuration file with environment variables
cat <<EOF > ${APP_DIR}/config.js
window.RUNTIME_CONFIG = {
  AUTH_DOMAIN: "${AUTH_DOMAIN:-}",
  AUTH_CLIENT_ID: "${AUTH_CLIENT_ID:-}",
  AUTH_AUDIENCE: "${AUTH_AUDIENCE:-}",
  AIFINDR_DOMAIN: "${AIFINDR_DOMAIN:-}"
};
EOF

echo "Configuration generated:"

# Iniciar Nginx
exec nginx -g "daemon off;" 