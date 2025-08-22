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

ARG OPENJDK_VERSION=17.0.16+8
ARG OPENJDK_RELEASE=1~deb12u1

COPY --chown=packager:packager\
    sources/openjdk-17_${OPENJDK_VERSION}-${OPENJDK_RELEASE}.dsc\
    sources/openjdk-17_${OPENJDK_VERSION}-${OPENJDK_RELEASE}.debian.tar.xz\
    sources/openjdk-17_${OPENJDK_VERSION}.orig-googletest.tar.xz\
    sources/openjdk-17_${OPENJDK_VERSION}.orig.tar.xz\
    sources/openjdk-17-jdk-headless_${OPENJDK_VERSION}-${OPENJDK_RELEASE}_amd64.deb\
    sources/openjdk-17-jre-headless_${OPENJDK_VERSION}-${OPENJDK_RELEASE}_amd64.deb\
    /home/packager/sources/

RUN set -xe\
 && cd ~/sources/\
 && dpkg-source -x openjdk-17_${OPENJDK_VERSION}-${OPENJDK_RELEASE}.dsc\
 && mv -v openjdk-17-${OPENJDK_VERSION} ~/\
 && ln -v openjdk-17_${OPENJDK_VERSION}.orig.tar.xz openjdk-17_${OPENJDK_VERSION}.orig-googletest.tar.xz ~/

# 安装依赖
RUN --mount=type=cache,target=/var/cache,sharing=private set -xe\
 && sudo apt-get update\
 && mkdir -p ~/deps/\
 && cd ~/deps/\
 && sudo apt-get install -y jtreg6\
    ~/sources/openjdk-17-jdk-headless_${OPENJDK_VERSION}-${OPENJDK_RELEASE}_amd64.deb\
    ~/sources/openjdk-17-jre-headless_${OPENJDK_VERSION}-${OPENJDK_RELEASE}_amd64.deb\
 && sudo mk-build-deps -i --tool='apt-get -y' ~/openjdk-17-${OPENJDK_VERSION}/debian/control

# sed修改
## s~bullseye~${VERSION_CODENAME}~g" -e "s~deb11~deb${VERSION_ID}~g: 修改发行版名称

# 构建（>30min）
RUN set -xe\
 && cd ~/openjdk-17-${OPENJDK_VERSION}\
 && . /etc/os-release\
 && sed -e "s~bookworm~${VERSION_CODENAME}~g" -e "s~deb12~deb${VERSION_ID}~g" debian/changelog -i\
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
