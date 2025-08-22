FROM debian:13 AS base-env

RUN --mount=type=cache,target=/var/cache,sharing=private set -xe\
 && . /etc/os-release\
 && sed -i "s~Suites:\( ${VERSION_CODENAME} .*\)~Suites:\1 ${VERSION_CODENAME}-backports~g" /etc/apt/sources.list.d/debian.sources\
 && echo 'Acquire::EnableSrvRecords "false";' > /etc/apt/apt.conf.d/docker-no-srv\
 && apt-get update\
 && apt-get install -y build-essential fakeroot devscripts sudo ca-certificates unzip wget curl vim\
 && useradd packager -m -s /bin/bash\
 && echo "packager ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/packager

# USER packager
# WORKDIR /home/packager

FROM base-env AS builder

COPY sources/ /root/sources/

ARG MYSQL_RELEASE=5.7.42-1debian10
ARG MYSQL_VERSION=5.7.44
RUN set -xe\
 && MYSQL_RVERSION=${MYSQL_RELEASE%%-*}\
 && MYSQL_MINOR=${MYSQL_RELEASE%.*}\
 && sudo mkdir -p /usr/global/share\
 && cd /usr/global/share\
 && sudo tar xf ~/sources/mysql-boost-${MYSQL_VERSION}.tar.gz mysql-${MYSQL_VERSION}/boost --strip-components=2\
 && cd ~/sources/\
 && dpkg-source -x mysql-community_${MYSQL_RELEASE}.dsc\
 && cd ~\
 && mkdir mysql-community-${MYSQL_VERSION}\
 && cd mysql-community-${MYSQL_VERSION}\
 && tar xf ~/sources/mysql-${MYSQL_VERSION}.tar.gz --strip-components=1\
 && tar xf ~/sources/mysql-community_${MYSQL_RELEASE}.debian.tar.xz\
 && grep -Ev '^$|^#' debian/patches/series | xargs -I {} patch -p1 -i debian/patches/{}\
 && sed "s~${MYSQL_RVERSION}~${MYSQL_VERSION}~g" -i debian/changelog\
 && ln -v ~/sources/mysql-${MYSQL_VERSION}.tar.gz ~/mysql-community_5.7.44.orig.tar.gz\
 && sed 's/dh-systemd//g' debian/control -i

RUN --mount=type=cache,target=/var/cache,sharing=private set -xe\
 && sudo apt-get update\
 && sudo apt-get install -y libncurses5-dev libssl-dev pkg-config libtirpc-dev cpp-12 g++-12 gcc-12 libgcc-12-dev\
 && mkdir ~/deps/\
 && cd ~/deps/\
 && sudo mk-build-deps -i --tool='apt-get -y' ~/mysql-community-${MYSQL_VERSION}/debian/control

# https://bugs.mysql.com/bug.php?id=100217
ADD patch-innodb_engine-fcommon.diff /root/sources/patch-innodb_engine-fcommon.diff
RUN set -xe\
 && cd ~/mysql-community-${MYSQL_VERSION}\
 && . /etc/os-release\
 && sed -e "s~debian10~debian${VERSION_ID}~g" -e "s~buster~${VERSION_CODENAME}~g" debian/changelog -i\
 && sed -e '/WITH_SSL/s/.*/\t\t-WITH_SSL=system \\/g' debian/rules -i\
 && echo "patch-innodb_engine-fcommon.diff" >> debian/patches/series\
 && ln -v ~/sources/patch-innodb_engine-fcommon.diff debian/patches/patch-innodb_engine-fcommon.diff\
 && patch -p1 -i debian/patches/patch-innodb_engine-fcommon.diff\
 && export CC=/usr/bin/gcc-12 export CXX=/usr/bin/g++-12\
 && dpkg-buildpackage -us -uc

FROM scratch AS exporter
COPY --from=builder\
    /root/*.deb\
    /root/*.buildinfo\
    /root/*.changes\
    /root/*.dsc\
    /root/*.debian.tar\
    /root/*.debian.tar.bz2\
    /root/*.debian.tar.gz\
    /root/*.debian.tar.xz\
    /root/*.orig*.tar\
    /root/*.orig*.tar.bz2\
    /root/*.orig*.tar.gz\
    /root/*.orig*.tar.xz\
    /
