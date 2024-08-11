FROM python:3.9 AS base
#
#  USAGE:
#     cd services/datawave
#     docker build -f Dockerfile -t datawave:prod --target production ../../
#     docker run datawave:prod
#

LABEL maintainer=neurogarg

# simcore-user uid=8004(${SC_USER_NAME}) gid=8004(${SC_USER_NAME}) groups=8004(${SC_USER_NAME})
ENV SC_USER_ID 8004
ENV SC_USER_NAME scu
RUN adduser --uid ${SC_USER_ID} --disabled-password --gecos "" --shell /bin/sh --home /home/${SC_USER_NAME} ${SC_USER_NAME}

RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    jq \
    git \
    curl \
    python3 \
    python3-pip \
    && rm --recursive --force /var/lib/apt/lists/*

# -------------------------- Build stage -------------------
# Installs build/package management tools and third party dependencies
#
# + /build             WORKDIR
#

FROM base AS build

ENV SC_BUILD_TARGET build


WORKDIR /build
# defines the output of the build
RUN mkdir --parents /build/bin
# copy src code to user
COPY --chown=${SC_USER_NAME}:${SC_USER_NAME} src/datawave src/datawave

## install the reuirements
RUN pip --no-cache --quiet install --upgrade pip && \
    pip install -r src/datawave/requirements.txt




# --------------------------Production stage -------------------
# Final cleanup up to reduce image size and startup setup
# Runs as ${SC_USER_NAME} (non-root user)
#
#  + /home/${SC_USER_NAME}     $HOME = WORKDIR
#    + datawave [${SC_USER_NAME}:${SC_USER_NAME}]
#    + docker [${SC_USER_NAME}:${SC_USER_NAME}]
#    + service.cli [${SC_USER_NAME}:${SC_USER_NAME}]
#
FROM base AS production

ENV SC_BUILD_TARGET production
ENV SC_BOOT_MODE production


ENV INPUT_FOLDER="/input" \
    OUTPUT_FOLDER="/output"


WORKDIR /home/${SC_USER_NAME}

# copy lib for python packages and the src files containing my code
COPY --from=build --chown=${SC_USER_NAME}:${SC_USER_NAME} /usr/local/lib /usr/local/lib

COPY --from=build --chown=${SC_USER_NAME}:${SC_USER_NAME} /build/src/datawave /home/${SC_USER_NAME}/datawave



# ------------------------------------------------------------------------------------
#TODO:
# Install runtime dependencies
RUN apt-get update \
&& apt-get -y install --no-install-recommends \
    zip \
&& rm -rf /var/lib/apt/lists/*
# ------------------------------------------------------------------------------------

# copy docker bootup scripts
COPY --chown=${SC_USER_NAME}:${SC_USER_NAME} docker/python/*.sh docker/
# copy simcore service cli
COPY --chown=${SC_USER_NAME}:${SC_USER_NAME} service.cli/ service.cli/
# necessary to be able to call run directly without sh in front
ENV PATH="/home/${SC_USER_NAME}/service.cli:${PATH}"




# ------------------------------------------------------------------------------------
#TODO:
# uncomment and provide a healtchecker if possible
# HEALTHCHECK --interval=30s \
#             --timeout=120s \
#             --start-period=30s \
#             --retries=3 \
#             CMD ["healthchecker app"]
# ------------------------------------------------------------------------------------

ENTRYPOINT [ "/bin/sh", "docker/entrypoint.sh", "/bin/sh", "-c" ]
CMD ["run"]
