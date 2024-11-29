FROM quay.io/centos/centos:7 AS centos7-env

RUN --mount=type=cache,target=/var/cache set -xe\
 && yum install -y '@Development Tools' rpmdevtools sudo ca-certificates unzip wget curl vim epel-release\
 && groupadd mock\
 && useradd mockbuild -m -G mock\
 && echo "mockbuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mockbuild\
 && sudo -u mockbuild -i 'rpmdev-setuptree'

USER mockbuild
WORKDIR /home/mockbuild

FROM centos7-env AS builder

# 安装依赖
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo yum install -y python-devel

# 安装源码包
ARG JAVAPACKAGES_SOURCE
RUN set -xe\
 && rpm -ivh ${JAVAPACKAGES_SOURCE}

# 安装依赖
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/javapackages-tools.spec

COPY ignore-python-tmpfile.patch /home/mockbuild/ignore-python-tmpfile.patch
# 构建（>30min）
RUN set -xe\
 && patch -d ~/rpmbuild/SPECS/ -p1 -i ~/ignore-python-tmpfile.patch\
 && rpmbuild -ba ~/rpmbuild/SPECS/javapackages-tools.spec

FROM scratch AS exporter
COPY --from=builder /home/mockbuild/rpmbuild/RPMS /RPMS
COPY --from=builder /home/mockbuild/rpmbuild/SRPMS /SRPMS
