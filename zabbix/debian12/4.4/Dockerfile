FROM debian:12 as base-env

RUN --mount=type=cache,target=/var/cache set -xe\
 && . /etc/os-release\
 && sed -i "s~Suites:\( ${VERSION_CODENAME} .*\)~Suites:\1 ${VERSION_CODENAME}-backports~g" /etc/apt/sources.list.d/debian.sources\
 && echo 'Acquire::EnableSrvRecords "false";' > /etc/apt/apt.conf.d/docker-no-srv\
 && apt-get update\
 && apt-get install -y build-essential fakeroot devscripts sudo ca-certificates unzip wget curl vim\
 && useradd packager -m -s /bin/bash\
 && echo "packager ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/packager

USER packager
WORKDIR /home/packager

FROM base-env as builder
ARG ZABBIX_VERSION=4.4.3
ARG ZABBIX_RELEASE=1+buster
RUN set -xe\
 && mkdir sources/\
 && cd sources/\
 && dget http://repo.zabbix.com/zabbix/4.4/debian/pool/main/z/zabbix/zabbix_${ZABBIX_VERSION}-${ZABBIX_RELEASE}.dsc\
 || dpkg-source -x zabbix_${ZABBIX_VERSION}-${ZABBIX_RELEASE}.dsc\
 && mv -v zabbix-${ZABBIX_VERSION} ../zabbix-${ZABBIX_VERSION}\
 && cp -v zabbix_${ZABBIX_VERSION}*orig*.tar.* ../

RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo apt-get update\
 && sudo apt-get install -y golang\
 && mkdir deps/\
 && cd deps/\
 && sudo mk-build-deps -i --tool='apt-get -y' ~/zabbix-${ZABBIX_VERSION}/debian/control

RUN set -xe\
 && cd ~/zabbix-${ZABBIX_VERSION}\
 && . /etc/os-release\
 && sed "s~buster~${VERSION_CODENAME}~g" debian/changelog -i\
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
