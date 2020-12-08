FROM docker.io/node:12-alpine

RUN apk add --no-cache \
    git \
    # npm package system dependencies
    autoconf \
    automake \
    build-base \
    libpng-dev \
    pngquant

RUN mkdir -p /openedx/app
WORKDIR /openedx/app

COPY ./bin /openedx/bin
RUN chmod a+x /openedx/bin/*
ENV PATH /openedx/bin:./node_modules/.bin:${PATH}

# Create environment file directories
RUN mkdir -p /openedx/env/production /openedx/env/development

# Source environment file at runtime
ENTRYPOINT ["docker-entrypoint.sh"]