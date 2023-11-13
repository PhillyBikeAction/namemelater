# Now we're going to build our actual application, but not the actual production
# image that it gets deployed into.
FROM python:3.11.6-slim-bookworm as build

# Define whether we're building a production or a development image. This will
# generally be used to control whether or not we install our development and
# test dependencies.
ARG DEVEL=no

# By default, Docker has special steps to avoid keeping APT caches in the layers, which
# is good, but in our case, we're going to mount a special cache volume (kept between
# builds), so we WANT the cache to persist.
RUN set -eux; \
    rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache;

# Install System level build requirements, this is done before
# everything else because these are rarely ever going to change.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    set -x \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        bash

# We create an /opt directory with a virtual environment in it to store our
# application in.
RUN set -x \
    && python3 -m venv /opt/namemelater

# Now that we've created our virtual environment, we'll go ahead and update
# our $PATH to refer to it first.
ENV PATH="/opt/namemelater/bin:${PATH}"

# Next, we want to update pip, setuptools, and wheel inside of this virtual
# environment to ensure that we have the latest versions of them.
# TODO: We use --require-hashes in our requirements files, but not here, making
#       the ones in the requirements files kind of a moot point. We should
#       probably pin these too, and update them as we do anything else.
RUN pip --no-cache-dir --disable-pip-version-check install --upgrade pip setuptools wheel

# We copy this into the docker container prior to copying in the rest of our
# application so that we can skip installing requirements if the only thing
# that has changed is the code itself.
COPY requirements /tmp/requirements

# Install our development dependencies if we're building a development install
# otherwise this will do nothing.
RUN --mount=type=cache,target=/root/.cache/pip \
    set -x \
    && if [ "$DEVEL" = "yes" ]; then pip --disable-pip-version-check install -r /tmp/requirements/dev.txt; fi


# Install the Python level requirements, this is done after copying
# the requirements but prior to copying code itself into the container so
# that code changes don't require triggering an entire install of all of
# the dependencies.
RUN --mount=type=cache,target=/root/.cache/pip \
    set -x \
    && pip --disable-pip-version-check \
            install --no-deps \
                    -r /tmp/requirements/main.txt \
    && pip check \
    && find /opt/namemelater -name '*.pyc' -delete


# Now we're going to build our actual application image, which will eventually
# pull in the static files that were built above.
FROM python:3.11.6-slim-bookworm

# Setup some basic environment variables that are ~never going to change.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH /opt/namemelater/src/
ENV PATH="/opt/namemelater/bin:${PATH}"

WORKDIR /opt/namemelater/src/

# Define whether we're building a production or a development image. This will
# generally be used to control whether or not we install our development and
# test dependencies.
ARG DEVEL=no

# This is a work around because otherwise postgresql-client bombs out trying
# to create symlinks to these directories.
RUN set -x \
    && mkdir -p /usr/share/man/man1 \
    && mkdir -p /usr/share/man/man7

# Install System level requirements, this is done before everything
# else because these are rarely ever going to change.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    set -x \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        bash \
        $(if [ "$DEVEL" = "yes" ]; then echo 'vim'; fi) \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the directory into the container, this is done last so that changes to
# code itself require the least amount of layers being invalidated from
# the cache. This is most important in development, but it also useful for
# deploying new code changes.
COPY --from=build /opt/namemelater/ /opt/namemelater/
COPY . /opt/namemelater/src/
