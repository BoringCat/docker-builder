ARG DEBIAN_RELEASE
FROM debian:${DEBIAN_RELEASE} AS debian-env

SHELL [ "/bin/bash", "-xeuo", "pipefail", "-c" ]

ARG ENABLE_BACKPORTS
ARG BACKPORTS_URL=http://deb.debian.org/debian
RUN --mount=type=cache,target=/var/cache,sharing=locked\
    source /etc/os-release\
 && if [ ! -z "${ENABLE_BACKPORTS:-}" ]; then\
    echo 'Types: deb'\
        "\nURIs: ${BACKPORTS_URL}"\
        "\nSuites: ${VERSION_CODENAME}-backports"\
        '\nComponents: main'\
        '\nSigned-By: /usr/share/keyrings/debian-archive-keyring.gpg'\
        | tee /etc/apt/sources.list.d/backports.sources;\
 fi\
 && echo 'Acquire::EnableSrvRecords "false";' > /etc/apt/apt.conf.d/docker-no-srv\
 && apt-get update\
 && apt-get install -y build-essential fakeroot devscripts sudo ca-certificates unzip wget curl vim\
 && useradd packager -m -s /bin/bash\
 && echo "packager ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/packager

USER packager
WORKDIR /home/packager
SHELL [ "/bin/bash", "-xeuo", "pipefail", "-c" ]

FROM debian-env AS builder

ARG REDIS_DSC
RUN \
    REDIS_DSC_FILE=${REDIS_DSC##*/}\
 && REDIS_MAJOR=${REDIS_DSC_FILE%_*}\
 && REDIS_VERSION=${REDIS_DSC_FILE##*_}\
 && REDIS_VERSION=${REDIS_VERSION%-*}\
 && printf "REDIS_DSC_FILE=%s\nREDIS_MAJOR=%s\nREDIS_VERSION=%s\n"\
    "${REDIS_DSC_FILE}"\
    "${REDIS_MAJOR}"\
    "${REDIS_VERSION}"\
    > ~/.build.env\
 && mkdir ~/sources/\
 && cd ~/sources/\
 && dget ${REDIS_DSC} || dpkg-source -x ${REDIS_DSC_FILE}\
 && mv -v ${REDIS_MAJOR}-${REDIS_VERSION} ../${REDIS_MAJOR}-${REDIS_VERSION}\
 && cp -v *.tar.* ../

RUN --mount=type=cache,target=/var/cache,sharing=locked\
    mkdir ~/deps/\
 && cd ~/deps/\
 && source ~/.build.env\
 && sudo apt-get update\
 && sudo mk-build-deps -i --tool='apt-get -y' ~/${REDIS_MAJOR}-${REDIS_VERSION}/debian/control

RUN source ~/.build.env\
 && source /etc/os-release\
 && cd ~/${REDIS_MAJOR}-${REDIS_VERSION}\
 && dpkg-buildpackage -us -uc

FROM scratch AS exporter
COPY --from=builder\
    /home/packager/*.deb\
    /home/packager/*.buildinfo\
    /home/packager/*.changes\
    /home/packager/*.dsc\
    /home/packager/*.debian.tar\
    /home/packager/*.debian.tar.bz2\
    /home/packager/*.debian.tar.gz\
    /home/packager/*.debian.tar.xz\
    /home/packager/*.orig*.tar\
    /home/packager/*.orig*.tar.bz2\
    /home/packager/*.orig*.tar.gz\
    /home/packager/*.orig*.tar.xz\
    /
