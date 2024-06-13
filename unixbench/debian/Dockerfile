ARG DEBIAN_RELEASE
FROM debian:${DEBIAN_RELEASE} as debian-env

ARG ENABLE_BACKPORTS
ARG BACKPORTS_URL=http://deb.debian.org/debian
RUN --mount=type=cache,target=/var/cache set -xe\
 && . /etc/os-release\
 && if [ ! -z "${ENABLE_BACKPORTS}" ]; then\
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

ARG UNIXBENCH_VERSION=5.1.3
FROM debian-env as builder
COPY --chown=packager:packager debian /home/packager/unixbench-${UNIXBENCH_VERSION}/debian

ARG COMMIT_SHA=a07fcc03264915c624f0e4818993c5b4df3fa703
RUN set -xe\
 && wget https://github.com/kdlucas/byte-unixbench/archive/${COMMIT_SHA}.tar.gz -O ~/unixbench_${UNIXBENCH_VERSION}.orig.tar.gz\
 && mkdir deps/\
 && cd deps/\
 && sudo mk-build-deps -i --tool='apt-get -y' ~/unixbench-${UNIXBENCH_VERSION}/debian/control

RUN set -xe\
 && cd ~/unixbench-${UNIXBENCH_VERSION}\
 && . /etc/os-release\
 && sed "s~bullseye~${VERSION_CODENAME}~g" debian/changelog -i\
 && ls -alhF ..\
 && tar xf ../unixbench_${UNIXBENCH_VERSION}.orig.tar.gz --strip-components=1\
 && cat debian/patches/series | xargs -I {} patch -p1 -i debian/patches/{}\
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
