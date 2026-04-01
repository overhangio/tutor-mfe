# syntax=docker/dockerfile:1
# https://hub.docker.com/_/node/tags
FROM docker.io/node:24.11.0-bullseye-slim AS base

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
    # required for building node-canvas (on arm, for authoring)
    # https://www.npmjs.com/package/canvas
    libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev

RUN mkdir -p /openedx/app /openedx/env
WORKDIR /openedx/app
ENV PATH=/openedx/app/node_modules/.bin:${PATH}

{{ patch("mfe-dockerfile-base") }}

{% for app_name, app in iter_mfes() %}
####################### {{ app_name }} MFE
######## {{ app_name }} (git)
FROM base AS {{ app_name }}-git
{#- Invalidate the build cache if a change is detected upstream #}
ADD --keep-git-dir=true {{ app["repository"] }}#{{ app.get("version", MFE_COMMON_VERSION) }} .

######## {{ app_name }} (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS {{ app_name }}-src
COPY --from={{ app_name }}-git /openedx/app /

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
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY
{{ patch("mfe-dockerfile-post-npm-install") }}
{{ patch("mfe-dockerfile-post-npm-install-{}".format(app_name)) }}
COPY --from={{ app_name }}-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository={{ ATLAS_REPOSITORY }} --revision={{ ATLAS_REVISION }} {{ ATLAS_OPTIONS }}" pull_translations

EXPOSE {{ app['port'] }}

# Configuration needed at build time
ENV APP_ID={{ app_name }}
ENV PUBLIC_PATH='/{{ app_name }}/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false
COPY env.config.jsx /openedx/app
{{ patch("mfe-dockerfile-pre-npm-build") }}
{{ patch("mfe-dockerfile-pre-npm-build-{}".format(app_name)) }}

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
{{ patch("mfe-dockerfile-post-npm-build") }}
{{ patch("mfe-dockerfile-post-npm-build-{}".format(app_name)) }}
{% endfor %}


{%- for site_name, app in iter_frontend_sites() %}
######## build of site-{{ site_name }}-git
FROM base AS site-{{ site_name }}-git
WORKDIR /openedx/site

# Either use site-local or the configured repository
{%- if app.get("repository") and app["repository"] == "local" %}
COPY frontend-site/ /openedx/site
{%- else %}
ADD --keep-git-dir=true {{ app["repository"] }}#{{ app.get("version", MFE_COMMON_VERSION) }} .
{%- endif %}
{%- endfor %}


{%- set ns = namespace(repos_exists=0) %}
{% for site_name, app in iter_frontend_sites() %}
######## build of site-{{ site_name }}-src
FROM base AS site-{{ site_name }}-src
WORKDIR /openedx/site/packages

# Git clone all frontend apps that should be built

{%- for app_name, app in iter_frontend_apps() %}
{%- if app.get("repository") %}
RUN git clone --depth 1 --branch {{ app.get("version", MFE_COMMON_VERSION) }} {{ app["repository"] }} frontend-app-{{ app_name }}
{%- set ns.repos_exists = 1 %}
{%- endif %}
{%- endfor %}

WORKDIR /openedx/site

COPY --from=site-{{ site_name }}-git /openedx/site/package.json /openedx/site

ARG NPM_REGISTRY={{ NPM_REGISTRY }}
{{ patch("frontend-site-dockerfile-pre-npm-install") }}

{# This one we need to optimize, so the copy doesn't trigger a new npm install when it's not required #}
RUN --mount=type=cache,target=/root/.npm-sites,sharing=shared npm install --no-audit --no-fund --registry=$NPM_REGISTRY

{{ patch("frontend-site-dockerfile-post-npm-install") }}

{%- endfor %}


{%- for site_name, app in iter_frontend_sites() %}
######## build of site-{{ site_name }}-common
FROM base AS site-{{ site_name }}-common
WORKDIR /openedx/site

COPY --from=site-{{ site_name }}-git /openedx/site/ /openedx/site
COPY --from=site-{{ site_name }}-src /openedx/site /openedx/site

{%- if ns.repos_exists %}
RUN npm run build:packages
{%- endif %}

{{ patch("frontend-site-dockerfile-pre-npm-build") }}
RUN PUBLIC_PATH="/site-{{ app.get("site", "default") }}/" npm run build
{{ patch("frontend-site-dockerfile-post-npm-build") }}

{%- endfor %}


####### final production image with all static assets
FROM {{ MFE_CADDY_DOCKER_IMAGE }} AS production

RUN mkdir -p /openedx/dist

# Copy static assets
{% for app_name, app in iter_mfes() %}
COPY --from={{ app_name }}-prod /openedx/app/dist /openedx/dist/{{ app_name }}
{% endfor %}

{% for site_name, app in iter_frontend_sites() %}
COPY --from=site-{{ site_name }}-common /openedx/site/dist /openedx/dist/site-{{ site_name }}
{% endfor %}

{{ patch("mfe-dockerfile-production-final") }}
