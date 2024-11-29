FROM centos:6 AS centos6-env

RUN --mount=type=cache,target=/var/cache set -xe\
 && yum install -y '@Development Tools' rpmdevtools sudo ca-certificates unzip wget curl vim epel-release\
   yum-utils\
 && useradd packager -m\
 && echo "packager ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/packager\
 && sudo -u packager -i 'rpmdev-setuptree'

USER packager
WORKDIR /home/packager

FROM centos6-env AS builder

RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo yum install -y sqlite-devel libxml2-devel OpenIPMI-devel libssh2-devel pcre2-devel\
    unixODBC-devel net-snmp-devel gnutls-devel openssl-devel libcurl-devel libevent-devel\
    openldap-devel mariadb-devel java-1.8.0-openjdk-devel

ARG MYSQL_KEY
ARG MYSQL_VERSION
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo rpm -ivh https://repo.mysql.com/${MYSQL_VERSION}-community-release-el6.rpm\
 && if [ ! -z "${MYSQL_KEY}" ]; then curl https://repo.mysql.com/${MYSQL_KEY}\
    | sudo tee /etc/pki/rpm-gpg/${MYSQL_KEY}\
    | sudo tee /etc/pki/rpm-gpg/RPM-GPG-KEY-mysql > /dev/null;\
    fi\
 && sudo yum install -y mysql-community-devel

ARG POSTGRESQL_VERSION
COPY postgresql-${POSTGRESQL_VERSION}/pgdg-archive.repo /etc/yum.repos.d/pgdg-archive.repo
COPY postgresql-${POSTGRESQL_VERSION}/patchs/ /home/packager/patchs/
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo yum install -y postgresql${POSTGRESQL_VERSION}-devel

# ARG GOLANG_VERSION
# RUN set -xe\
#  && wget https://go.dev/dl/go${GOLANG_VERSION}.linux-amd64.tar.gz\
#  && tar xf go${GOLANG_VERSION}.linux-amd64.tar.gz\
#  && sudo mv go /usr/lib/golang\
#  && sudo chown root:root -R /usr/lib/golang\
#  && sudo ln -sv /usr/lib/golang/bin/* /usr/bin/\
#  && rm go${GOLANG_VERSION}.linux-amd64.tar.gz

ARG ZABBIX_SRC
RUN --mount=type=cache,target=/var/cache set -xe\
 && rpm -ivh ${ZABBIX_SRC}\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/zabbix.spec

COPY patchs/ /home/packager/patchs/
ARG ZABBIX_BUILD_AGENT=1
ARG ZABBIX_BUILD_AGENT2=0
ARG ZABBIX_BUILD_FRONTEND=0
ARG ZABBIX_BUILD_JAVA_GATEWAY=1
ARG ZABBIX_BUILD_PROXY=1
ARG ZABBIX_BUILD_SERVER=0
ARG ZABBIX_WITH_MYSQL=1
ARG ZABBIX_WITH_PGSQL=1
ARG ZABBIX_WITH_SQLITE=1
RUN set -xe\
 && /bin/bash ~/patchs/choise_patch.sh\
 && rpmbuild -ba ~/rpmbuild/SPECS/zabbix.spec\
    -D "build_agent ${ZABBIX_BUILD_AGENT}"\
    -D "build_agent2 ${ZABBIX_BUILD_AGENT2}"\
    -D "build_frontend ${ZABBIX_BUILD_FRONTEND}"\
    -D "build_java_gateway ${ZABBIX_BUILD_JAVA_GATEWAY}"\
    -D "build_proxy ${ZABBIX_BUILD_PROXY}"\
    -D "build_server ${ZABBIX_BUILD_SERVER}"\
    -D "build_with_mysql ${ZABBIX_WITH_MYSQL}"\
    -D "build_with_pgsql ${ZABBIX_WITH_PGSQL}"\
    -D "build_with_sqlite ${ZABBIX_WITH_SQLITE}"

FROM scratch AS exporter
COPY --from=builder /home/packager/rpmbuild/RPMS /RPMS
COPY --from=builder /home/packager/rpmbuild/SRPMS /SRPMS
