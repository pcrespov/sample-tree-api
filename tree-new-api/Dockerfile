FROM python:3.6-alpine as base
#
#  USAGE:
#     cd sercices/tree-new-api
#     docker build -f Dockerfile -t tree-new-api:prod --target production ../../
#     docker run tree-new-api:prod
#
#  REQUIRED: context expected at ``osparc-simcore/`` folder because we need access to osparc-simcore/packages

LABEL maintainer=pcrespov

# simcore-user uid=8004(scu) gid=8004(scu) groups=8004(scu)
RUN adduser -D -u 8004 -s /bin/sh -h /home/scu scu

RUN apk add --no-cache \
      su-exec

ENV PATH "/home/scu/.local/bin:$PATH"

# All SC_ variables are customized
ENV SC_PIP pip3 --no-cache-dir
ENV SC_BUILD_TARGET base

EXPOSE 8080


# -------------------------- Build stage -------------------
# Installs build/package management tools and third party dependencies
#
# + /build             WORKDIR
#


FROM base as build

ENV SC_BUILD_TARGET build


RUN apk add --no-cache \
      # postgresql-dev \
      # libc-dev \
      # libffi-dev \
      gcc \
      git

RUN $SC_PIP install --upgrade \
      pip \
      wheel \
      setuptools

WORKDIR /build

# install base 3rd party dependencies
COPY  services/tree-new-api/requirements/*.txt \
      services/tree-new-api/requirements/

RUN $SC_PIP install \
      -r services/tree-new-api/requirements/base.txt


# --------------------------Cache stage -------------------
# CI in master buils & pushes this target to speed-up image build
#
#  + /build
#    + services/tree-new-api [scu:scu] WORKDIR
#
FROM build as cache

ENV SC_BUILD_TARGET cache


COPY --chown=scu:scu packages /build/packages
COPY --chown=scu:scu services/tree-new-api /build/services/tree-new-api

WORKDIR /build/services/tree-new-api


RUN $SC_PIP install . &&\
    $SC_PIP list -v


# --------------------------Production stage -------------------
# Final cleanup up to reduce image size and startup setup
# Runs as scu (non-root user)
#
#  + /home/scu     $HOME = WORKDIR
#    + services/tree-new-api [scu:scu]
#
FROM cache as production

ENV SC_BUILD_TARGET production
ENV SC_BOOT_MODE production

WORKDIR /home/scu

RUN mkdir -p services/tree-new-api &&\
    chown scu:scu services/tree-new-api &&\
    mv /build/services/tree-new-api/docker services/tree-new-api/docker &&\
    rm -rf /build


RUN apk del --no-cache\
      gcc \
      git


HEALTHCHECK --interval=30s \
            --timeout=20s \
            --start-period=30s \
            --retries=3 \
            CMD ["python3", "services/tree-new-api/docker/healthcheck.py", "http://localhost:8080/v0/"]

ENTRYPOINT [ "/bin/sh", "services/tree-new-api/docker/entrypoint.sh" ]
CMD ["/bin/sh", "services/tree-new-api/docker/boot.sh"]


# --------------------------Development stage -------------------
# Source code accessible in host but runs in container
# Runs as myu with same gid/uid as host
# Placed at the end to speed-up the build if images targeting production
#
#  + /devel         WORKDIR
#    + services  (mounted volume)
#
FROM build as development

ENV SC_BUILD_TARGET development
ENV SC_BOOT_MODE development




WORKDIR /build


WORKDIR /devel
VOLUME  /devel/packages
VOLUME  /devel/services/tree-new-api/

ENTRYPOINT ["/bin/sh", "services/tree-new-api/docker/entrypoint.sh"]
CMD ["/bin/sh", "services/tree-new-api/docker/boot.sh"]
