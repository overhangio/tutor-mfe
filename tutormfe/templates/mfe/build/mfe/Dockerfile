# https://hub.docker.com/_/node/tags
FROM docker.io/node:18.16.0-bullseye-slim AS base

RUN apt update \
  && apt install -y git \
    # required for cwebp-bin
    gcc libgl1 libxi6 make \
    # required for gifsicle, mozjpeg, and optipng (on arm)
    autoconf libtool pkg-config zlib1g-dev \
    # required for node-sass (on arm)
    python g++ \
    # required for image-webpack-loader (on arm)
    libpng-dev \
    # required for building node-canvas (on arm, for course-authoring)
    # https://www.npmjs.com/package/canvas
    libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev

RUN mkdir -p /openedx/app /openedx/env
WORKDIR /openedx/app
ENV PATH ./node_modules/.bin:${PATH}

######## i18n strings
FROM base AS i18n
COPY ./i18n /openedx/i18n
RUN chmod a+x /openedx/i18n/*.js
RUN echo "copying i18n data" \
  {%- for app_name, app in iter_mfes() %}
  && mkdir -p /openedx/i18n/{{ app_name }} \
  {%- endfor %}
  echo "done."

{% for app_name, app in iter_mfes() %}
####################### {{ app_name }} MFE
######## {{ app_name }} (git)
FROM base AS {{ app_name }}-git
{#- Invalidate the build cache if a change is detected upstream #}
{%- if app.get("refs") %}
ADD {{ app["refs"] }}/{{ app.get("version", MFE_COMMON_VERSION) }} /tmp/gitref-{{ app_name }}
{%- endif %}
RUN git clone {{ app["repository"] }} --branch {{ app.get("version", MFE_COMMON_VERSION) }} --depth 1 .

######## {{ app_name }} (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as {{ app_name }}-src
COPY --from={{ app_name }}-git /openedx/app /

######## {{ app_name }} (i18n)
FROM base AS {{ app_name }}-i18n
COPY --from={{ app_name }}-src / /openedx/app
COPY --from=i18n /openedx/i18n/{{ app_name }} /openedx/i18n/{{ app_name }}
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/{{ app_name }} /openedx/app/src/i18n/messages

######## {{ app_name }} (common)
FROM base AS {{ app_name }}-common
COPY --from={{ app_name }}-src /package.json /openedx/app/package.json
COPY --from={{ app_name }}-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY={{ NPM_REGISTRY }}
{{ patch("mfe-dockerfile-pre-npm-install") }}
{{ patch("mfe-dockerfile-pre-npm-install-{}".format(app_name)) }}
{#- Required for building optipng on M1 #}
ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
{#- We define this environment variable to bypass an issue with the installation of pact https://github.com/pact-foundation/pact-js-core/issues/264 #}
ENV PACT_SKIP_BINARY_INSTALL=true
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/root/.npm,sharing=shared {% endif %}npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY
{{ patch("mfe-dockerfile-post-npm-install") }}
{{ patch("mfe-dockerfile-post-npm-install-{}".format(app_name)) }}
COPY --from={{ app_name }}-src / /openedx/app
COPY --from={{ app_name }}-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages
EXPOSE {{ app['port'] }}

# Configuration needed at build time
ENV APP_ID={{ app_name }}
ENV PUBLIC_PATH='/{{ app_name }}/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false

######## {{ app_name }} (dev)
FROM {{ app_name }}-common AS {{ app_name }}-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]
{% endfor %}

# Production images are last to accelerate dev image building
{%- for app_name, app in iter_mfes() %}
######## {{ app_name }} (production)
FROM {{ app_name }}-common AS {{ app_name }}-prod
ENV NODE_ENV=production
RUN npm run build
{% endfor %}

####### final production image with all static assets
FROM {{ MFE_CADDY_DOCKER_IMAGE }} as production

RUN mkdir -p /openedx/dist

# Copy static assets
{% for app_name, app in iter_mfes() %}
COPY --from={{ app_name }}-prod /openedx/app/dist /openedx/dist/{{ app_name }}
{% endfor %}
