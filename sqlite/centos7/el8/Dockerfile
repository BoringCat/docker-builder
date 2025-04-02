FROM quay.io/centos/centos:7 AS centos-env

COPY repos/ /etc/yum.repos.d/

RUN --mount=type=cache,target=/var/cache set -xe\
 && yum install -y epel-release --disablerepo=epel\
 && yum install -y '@Development Tools' rpmdevtools sudo ca-certificates unzip wget curl vim epel-release\
 && groupadd mock\
 && useradd mockbuild -m -G mock\
 && echo "mockbuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mockbuild\
 && sudo -u mockbuild -i 'rpmdev-setuptree'

USER mockbuild
WORKDIR /home/mockbuild

FROM centos-env AS builder

# 安装依赖
COPY rpms/ /tmp/rpms/
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo yum install -y zlib-devel\
 && sudo yum install -y /tmp/rpms/tcl-*.rpm

# 安装依赖并构建 sqlite
ARG SQLITE_SOURCE
RUN --mount=type=cache,target=/var/cache set -xe\
 && rpm -ivh ${SQLITE_SOURCE}\
 && sed -i 's~%ldconfig_scriptlets \(.*\)$~%post \1 -p /sbin/ldconfig\n%postun \1 -p /sbin/ldconfig~g' ~/rpmbuild/SPECS/sqlite.spec\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/sqlite.spec

# 构建 sqlite
RUN --mount=type=cache,target=/var/cache set -xe\
 && rpmbuild -ba ~/rpmbuild/SPECS/sqlite.spec

FROM scratch AS exporter
COPY --from=builder /home/mockbuild/rpmbuild/RPMS /RPMS
COPY --from=builder /home/mockbuild/rpmbuild/SRPMS /SRPMS
