FROM node:lts-alpine AS builder

WORKDIR /frontend

ADD . /frontend

RUN npm i && npx vite build

FROM caddy:2.6-alpine

RUN sed -i 's|/usr/share/caddy|/var/www/html|g' /etc/caddy/Caddyfile

COPY --from=builder /frontend/dist /var/www/html
