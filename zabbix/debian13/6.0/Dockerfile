FROM debian:13 AS base-env

RUN --mount=type=cache,target=/var/cache,sharing=private set -xe\
 && . /etc/os-release\
 && sed -i "s~Suites:\( ${VERSION_CODENAME} .*\)~Suites:\1 ${VERSION_CODENAME}-backports~g" /etc/apt/sources.list.d/debian.sources\
 && echo 'Acquire::EnableSrvRecords "false";' > /etc/apt/apt.conf.d/docker-no-srv\
 && apt-get update\
 && apt-get install -y build-essential fakeroot devscripts sudo ca-certificates unzip wget curl vim\
 && useradd packager -m -s /bin/bash\
 && echo "packager ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/packager

USER packager
WORKDIR /home/packager

FROM base-env AS builder
ARG ZABBIX_VERSION
ARG ZABBIX_PACKNUM=1
ARG ZABBIX_SOURCE_RELEASE=12
ARG OPENJDK_MAJOR=17
ARG OPENJDK_VERSION=17.0.16+8-1~deb13u1_amd64
# 传输源码
COPY --chown=packager:packager\
    sources/zabbix_${ZABBIX_VERSION}-${ZABBIX_PACKNUM}+debian${ZABBIX_SOURCE_RELEASE}.dsc\
    sources/zabbix_${ZABBIX_VERSION}-${ZABBIX_PACKNUM}+debian${ZABBIX_SOURCE_RELEASE}.debian.tar.xz\
    sources/zabbix_${ZABBIX_VERSION}.orig.tar.gz\
    sources/openjdk-${OPENJDK_MAJOR}-jdk_${OPENJDK_VERSION}.deb\
    sources/openjdk-${OPENJDK_MAJOR}-jdk-headless_${OPENJDK_VERSION}.deb\
    sources/openjdk-${OPENJDK_MAJOR}-jre_${OPENJDK_VERSION}.deb\
    sources/openjdk-${OPENJDK_MAJOR}-jre-headless_${OPENJDK_VERSION}.deb\
    /home/packager/sources/

# 安装依赖
RUN --mount=type=cache,target=/var/cache,sharing=private set -xe\
 && cd ~/sources/\
 && dpkg-source -x zabbix_${ZABBIX_VERSION}-${ZABBIX_PACKNUM}+debian${ZABBIX_SOURCE_RELEASE}.dsc\
 && mv -v zabbix-${ZABBIX_VERSION} ~/\
 && ln -v zabbix_${ZABBIX_VERSION}.orig.tar.gz ~/\
 && mkdir -p ~/deps/\
 && cd ~/deps/\
 && sudo apt-get update\
 && sudo apt-get -y install ~/sources/openjdk-${OPENJDK_MAJOR}-*_${OPENJDK_VERSION}.deb\
 && sudo mk-build-deps -i --tool='apt-get -y' ~/zabbix-${ZABBIX_VERSION}/debian/control\
 && sudo apt-get -y install golang

# sed修改
## s~debian${ZABBIX_SOURCE_RELEASE}~debian${VERSION_ID}~g: 修改发行版名称
## s~default-jre-headless~java-sdk-headless (>=${OPENJDK_MAJOR})~g: 修改JDK版本，根据构建版本来定

# 构建
RUN set -xe\
 && cd ~/zabbix-${ZABBIX_VERSION}\
 && . /etc/os-release\
 && sed -i debian/changelog\
    -e "s~debian${ZABBIX_SOURCE_RELEASE}~debian${VERSION_ID}~g"\
 && sed -i debian/control\
    -e "s~default-jre-headless~java-sdk-headless (>=${OPENJDK_MAJOR})~g"\
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
