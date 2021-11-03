FROM docker.io/node:12-bullseye-slim AS base

RUN apt update \
  && apt install -y git

RUN mkdir -p /openedx/app
WORKDIR /openedx/app

ENV PATH ./node_modules/.bin:${PATH}

# Create environment file directories
RUN mkdir -p /openedx/env

{% for app in iter_values_named(suffix="MFE_APP") %}
######## {{ app["name"] }} (dev)
FROM base AS {{ app["name"] }}-dev
RUN git clone {{ app["repository"] }} --branch {{ app.get("version", MFE_COMMON_VERSION) }} --depth 1 .
ARG NPM_REGISTRY=https://registry.npmjs.org/
{{ patch("mfe-dockerfile-pre-npm-install") }}
RUN npm install --verbose --registry=$NPM_REGISTRY
{{ patch("mfe-dockerfile-post-npm-install") }}
ENV PUBLIC_PATH='/{{ app["name"] }}/'
EXPOSE {{ app['port'] }}
CMD ["npm", "run", "start"]
######## {{ app["name"] }} (production)
FROM {{ app["name"] }}-dev AS {{ app["name"] }}
COPY ./env/production /openedx/env/production
{% if "env" in app and "production" in app["env"] %}{% for key, value in app["env"]["production"].items() %}
ENV {{ key }}={{ value }}
{% endfor %}{% endif %}
RUN sh -c "set -a && . /openedx/env/production && npm run build"
{% endfor %}

####### final production image with all static assets
FROM docker.io/caddy:2.4.3-alpine

RUN mkdir -p /openedx/dist

# Copy static assets
{% for app in iter_values_named(suffix="MFE_APP") %}
COPY --from={{ app["name"] }} /openedx/app/dist /openedx/dist/{{ app["name"] }}
{% endfor %}

# Copy caddy config file
COPY ./Caddyfile /etc/caddy/Caddyfile
