# syntax=docker/dockerfile:1
# https://hub.docker.com/_/node/tags
ARG NODE_IMAGE=docker.io/node:24.14.1-bullseye-slim
FROM $NODE_IMAGE AS base

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

{#- TODO(legacy-mfe-removal): drop the entire per-MFE section below (all stages
    through the per-MFE production loop), plus the per-MFE asset copy in the
    final production stage at the end of this file. #}
{% for mfe_name, mfe in iter_mfes() %}
####################### {{ mfe_name }} MFE
######## {{ mfe_name }} (src)
# Empty layer with just the repo at the root, for build-time bind-mounts.
# Cache is invalidated when the upstream commit SHA changes.
FROM scratch AS {{ mfe_name }}-src
ADD --keep-git-dir=true {{ mfe["repository"] }}#{{ mfe.get("version", MFE_COMMON_VERSION) }} .

######## {{ mfe_name }} (common)
FROM base AS {{ mfe_name }}-common
COPY --from={{ mfe_name }}-src /package.json /package-lock.json /openedx/app/
ARG NPM_REGISTRY={{ NPM_REGISTRY }}
{{ patch("mfe-dockerfile-pre-npm-install") }}
{{ patch("mfe-dockerfile-pre-npm-install-{}".format(mfe_name)) }}
{#- Required for building optipng on M1 #}
ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
{#- We define this environment variable to bypass an issue with the installation of pact https://github.com/pact-foundation/pact-js-core/issues/264 #}
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY
{{ patch("mfe-dockerfile-post-npm-install") }}
{{ patch("mfe-dockerfile-post-npm-install-{}".format(mfe_name)) }}
COPY --from={{ mfe_name }}-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository={{ ATLAS_REPOSITORY }} --revision={{ ATLAS_REVISION }} {{ ATLAS_OPTIONS }}" pull_translations

EXPOSE {{ mfe['port'] }}

# Configuration needed at build time
ENV APP_ID={{ mfe_name }}
ENV PUBLIC_PATH='/{{ mfe_name }}/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false
COPY env.config.jsx /openedx/app
{{ patch("mfe-dockerfile-pre-npm-build") }}
{{ patch("mfe-dockerfile-pre-npm-build-{}".format(mfe_name)) }}

######## {{ mfe_name }} (dev)
FROM {{ mfe_name }}-common AS {{ mfe_name }}-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]
{% endfor %}

# Production images are last to accelerate dev image building
{%- for mfe_name, mfe in iter_mfes() %}
######## {{ mfe_name }} (production)
FROM {{ mfe_name }}-common AS {{ mfe_name }}-prod
ENV NODE_ENV=production
RUN npm run build
{{ patch("mfe-dockerfile-post-npm-build") }}
{{ patch("mfe-dockerfile-post-npm-build-{}".format(mfe_name)) }}
{% endfor %}

{%- for app_name, app in iter_frontend_apps() %}
######## frontend-app-{{ app_name }} (src)
FROM scratch AS frontend-app-{{ app_name }}-src
{%- if app.get("source") %}
{%- if app["source"].startswith("file://") %}
COPY {{ app["source"].removeprefix("file://") }} .
{%- else %}
ADD --keep-git-dir=true {{ app["source"] }} .
{%- endif %}
{%- endif %}
{% endfor %}

# No need to build the frontend site if there are no frontend apps.
{%- if get_frontend_apps() %}
####################### site
######## site (src)
FROM scratch AS site-src
{%- if MFE_SITE_REPOSITORY %}
ADD --keep-git-dir=true {{ MFE_SITE_REPOSITORY }}{{ "#" + MFE_SITE_VERSION if MFE_SITE_VERSION }} .
{%- else %}
COPY site/ .
{%- endif %}

######## site (common)
FROM base AS site-common
WORKDIR /openedx/site

# Copy frontend app packages into the workspace.
{%- for app_name, app in iter_frontend_apps() %}
COPY --from=frontend-app-{{ app_name }}-src / /openedx/site/packages/frontend-app-{{ app_name }}
{%- endfor %}

# Copy only package.json and package-lock.json first so that npm install is cached independently of source changes
COPY --from=site-src /package.json /package-lock.json ./

ARG NPM_REGISTRY={{ NPM_REGISTRY }}
{{ patch("mfe-dockerfile-pre-npm-install-site") }}
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install --no-audit --no-fund --registry=$NPM_REGISTRY
{{ patch("mfe-dockerfile-post-npm-install-site") }}

# Copy the full source; done after npm install so that source changes don't invalidate the install cache
COPY --from=site-src / .

RUN make ATLAS_OPTIONS="--repository={{ ATLAS_REPOSITORY }} --revision={{ ATLAS_REVISION }} {{ ATLAS_OPTIONS }}" pull_translations

######## mfe (dev)
FROM site-common AS mfe-dev
ENV NODE_ENV=development
EXPOSE {{ MFE_SITE_PORT }}
CMD ["/bin/bash", "-c", "npm run dev:packages"]

######## site (production)
FROM site-common AS site-prod
{{ patch("mfe-dockerfile-pre-npm-build-site") }}
RUN npm run build:packages
RUN npm run build
{{ patch("mfe-dockerfile-post-npm-build-site") }}

######## site (lockfile)
# Dedicated stage for updating the site's package-lock. Invoked by
# `tutor mfe update-site-lockfile`.
FROM $NODE_IMAGE AS site-lockfile-builder
WORKDIR /openedx/site
{%- for app_name, app in iter_frontend_apps() if app.get("source") %}
COPY --from=frontend-app-{{ app_name }}-src /package.json packages/frontend-app-{{ app_name }}/
{%- endfor %}
COPY --from=site-src /package.json /package-lock.json ./
ARG NPM_REGISTRY={{ NPM_REGISTRY }}
ARG NPM_UPDATE_PACKAGES=""
RUN npm update --no-audit --no-fund --package-lock-only --registry=$NPM_REGISTRY $NPM_UPDATE_PACKAGES

FROM scratch AS site-lockfile
COPY --from=site-lockfile-builder /openedx/site/package-lock.json /
{%- endif %}

####### final production image with all static assets
FROM {{ MFE_CADDY_DOCKER_IMAGE }} AS production

RUN mkdir -p /openedx/dist

# Copy static assets
{#- TODO(legacy-mfe-removal): drop this per-MFE asset copy loop. #}
{% for app_name, app in iter_mfes() %}
COPY --from={{ app_name }}-prod /openedx/app/dist /openedx/dist/{{ app_name }}
{% endfor %}

{%- if get_frontend_apps() %}
COPY --from=site-prod /openedx/site/dist /openedx/dist/site
{%- endif %}

{{ patch("mfe-dockerfile-production-final") }}
