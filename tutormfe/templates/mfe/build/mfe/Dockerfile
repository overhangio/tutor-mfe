FROM docker.io/node:12-bullseye-slim AS base

RUN apt update \
    && apt install -y git

RUN mkdir -p /openedx/app /openedx/env
WORKDIR /openedx/app
ENV PATH ./node_modules/.bin:${PATH}

{% for app in iter_values_named(suffix="MFE_APP") %}
######## {{ app["name"] }} (src)
FROM base AS {{ app["name"] }}-src
RUN git clone {{ app["repository"] }} --branch {{ app.get("version", MFE_COMMON_VERSION) }} --depth 1 .
######## {{ app["name"] }} (dev)
FROM base AS {{ app["name"] }}-dev
COPY --from={{ app["name"] }}-src /openedx/app/package.json /openedx/app/package.json
COPY --from={{ app["name"] }}-src /openedx/app/package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/
{{ patch("mfe-dockerfile-pre-npm-install") }}
RUN npm install --no-audit --no-fund --registry=$NPM_REGISTRY && rm -rf ~/.npm
{{ patch("mfe-dockerfile-post-npm-install") }}
COPY --from={{ app["name"] }}-src /openedx/app /openedx/app
ENV PUBLIC_PATH='/{{ app["name"] }}/'
EXPOSE {{ app['port'] }}
CMD ["npm", "run", "start"]
######## {{ app["name"] }} (production)
FROM {{ app["name"] }}-dev AS {{ app["name"] }}
COPY ./env/production /openedx/env/production
{% for key, value in app.get("env", {}).get("production", {}).items() %}
ENV {{ key }}={{ value }}
{% endfor %}
RUN bash -c "set -a && . /openedx/env/production && npm run build"
{% endfor %}

####### final production image with all static assets
FROM docker.io/caddy:2.4.3-alpine as production

RUN mkdir -p /openedx/dist

# Copy static assets
{% for app in iter_values_named(suffix="MFE_APP") %}
COPY --from={{ app["name"] }} /openedx/app/dist /openedx/dist/{{ app["name"] }}
{% endfor %}

# Copy caddy config file
COPY ./Caddyfile /etc/caddy/Caddyfile
