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

FROM debian-env as builder

ARG MYSQL_RELEASE=5.7.42-1debian10
RUN set -xe\
 && MYSQL_VERSION=${MYSQL_RELEASE%%-*}\
 && MYSQL_MINOR=${MYSQL_RELEASE%.*}\
 && mkdir ~/sources/\
 && cd ~/sources/\
 && dget http://repo.mysql.com/apt/debian/pool/mysql-${MYSQL_MINOR}/m/mysql-community/mysql-community_${MYSQL_RELEASE}.dsc\
 || dpkg-source -x mysql-community_${MYSQL_RELEASE}.dsc\
 && curl -L https://dev.mysql.com/get/Downloads/MySQL-${MYSQL_MINOR}/mysql-boost-${MYSQL_VERSION}.tar.gz -o /tmp/mysql-boost-${MYSQL_VERSION}.tar.gz\
 && sudo mkdir -p /usr/global/share\
 && cd /usr/global/share\
 && sudo tar xf /tmp/mysql-boost-${MYSQL_VERSION}.tar.gz mysql-5.7.42/boost --strip-components=2\
 && cd ~/sources\
 && . /etc/os-release\
 && if [ "${VERSION_CODENAME}" != "buster" ]; then sed 's/dh-systemd//g' mysql-community-${MYSQL_VERSION}/debian/control -i; fi\
 && mv -v mysql-community-${MYSQL_VERSION} ../mysql-community-${MYSQL_VERSION}\
 && cp -v *.tar.* ../

RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo apt-get update\
 && sudo apt-get install -y libncurses5-dev libssl-dev pkg-config\
 && mkdir deps/\
 && cd deps/\
 && sudo mk-build-deps -i --tool='apt-get -y' ~/mysql-community-*/debian/control

# https://bugs.mysql.com/bug.php?id=100217
ADD --chown=packager:packager patch-innodb_engine-fcommon.diff /tmp/patch-innodb_engine-fcommon.diff
RUN set -xe\
 && cd ~/mysql-community-*\
 && . /etc/os-release\
 && sed -e "s~debian10~debian${VERSION_ID}~g"\
    -e "s~buster~${VERSION_CODENAME}~g"\
    debian/changelog -i\
 && sed -e '/WITH_SSL/s/.*/\t\t-WITH_SSL=system \\/g'\
    debian/rules -i\
 && echo "patch-innodb_engine-fcommon.diff" >> debian/patches/series\
 && mv -v /tmp/patch-innodb_engine-fcommon.diff debian/patches/patch-innodb_engine-fcommon.diff\
 && patch -p1 -i debian/patches/patch-innodb_engine-fcommon.diff\
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
