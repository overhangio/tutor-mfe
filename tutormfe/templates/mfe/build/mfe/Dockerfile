FROM docker.io/node:12-bullseye-slim AS base

RUN apt update \
  && apt install -y git \
    # required for cwebp-bin
    gcc git libgl1 libxi6 make \
    # additionally required for gifsicle, mozjpeg, and optipng (on arm)
    autoconf libtool pkg-config zlib1g-dev \
    # additionally required for node-sass (on arm)
    python g++

RUN mkdir -p /openedx/app /openedx/env
WORKDIR /openedx/app
ENV PATH ./node_modules/.bin:${PATH}

######## i18n strings
FROM base AS i18n
COPY ./i18n /openedx/i18n
RUN chmod a+x /openedx/i18n/*.js
RUN echo "copying i18n data" \
  {%- for app in iter_values_named(suffix="MFE_APP") %}
  && mkdir -p /openedx/i18n/{{ app["name"] }} \
  {%- endfor %}
  echo "done."

{% for app in iter_values_named(suffix="MFE_APP") %}
######## {{ app["name"] }} (src)
FROM base AS {{ app["name"] }}-src
RUN git clone {{ app["repository"] }} --branch {{ app.get("version", MFE_COMMON_VERSION) }} --depth 1 .
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
######## {{ app["name"] }} (i18n)
FROM base AS {{ app["name"] }}-i18n
COPY --from={{ app["name"] }}-src /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages
COPY --from=i18n /openedx/i18n/{{ app["name"] }} /openedx/i18n/{{ app["name"] }}
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/{{ app["name"] }} /openedx/app/src/i18n/messages
######## {{ app["name"] }} (dev)
FROM base AS {{ app["name"] }}-dev

COPY --from={{ app["name"] }}-src /openedx/app/package.json /openedx/app/package.json
COPY --from={{ app["name"] }}-src /openedx/app/package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/
{{ patch("mfe-dockerfile-pre-npm-install") }}
{# Required for building optipng on M1 #}
ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
{# We define this environment variable to bypass an issue with the installation of pact https://github.com/pact-foundation/pact-js-core/issues/264 #}
ENV PACT_SKIP_BINARY_INSTALL=true
RUN npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY \
  && rm -rf ~/.npm
{{ patch("mfe-dockerfile-post-npm-install") }}
COPY --from={{ app["name"] }}-src /openedx/app /openedx/app
COPY --from={{ app["name"] }}-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages
ENV PUBLIC_PATH='/{{ app["name"] }}/'
EXPOSE {{ app['port'] }}
CMD ["npm", "run", "start"]
######## {{ app["name"] }} (production)
FROM {{ app["name"] }}-dev AS {{ app["name"] }}
COPY ./env/production /openedx/env/production
RUN touch /openedx/env/production.override \
  {%- for key, value in app.get("env", {}).get("production", {}).items() %}
  && echo "{{ key }}='{{ value }}'" >> /openedx/env/production.override \
  {%- endfor %}
  && echo "done setting production overrides"
RUN bash -c "set -a && source /openedx/env/production && source /openedx/env/production.override && npm run build"
{% endfor %}

####### final production image with all static assets
FROM {{ MFE_CADDY_DOCKER_IMAGE }} as production

RUN mkdir -p /openedx/dist

# Copy static assets
{% for app in iter_values_named(suffix="MFE_APP") %}
COPY --from={{ app["name"] }} /openedx/app/dist /openedx/dist/{{ app["name"] }}
{% endfor %}

# Copy caddy config file
COPY ./Caddyfile /etc/caddy/Caddyfile
