FROM quay.io/centos/centos:7 as centos7-env

RUN --mount=type=cache,target=/var/cache set -xe\
 && yum install -y '@Development Tools' rpmdevtools sudo ca-certificates unzip wget curl vim epel-release\
 && groupadd mock\
 && useradd mockbuild -m -G mock\
 && echo "mockbuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mockbuild\
 && sudo -u mockbuild -i 'rpmdev-setuptree'

USER mockbuild
WORKDIR /home/mockbuild

FROM centos7-env as builder

# # 安装依赖
# RUN --mount=type=cache,target=/var/cache set -xe\
#  && sudo yum install -y python-devel

# 安装源码包
ARG COPY_JDK_CONFIGS_SOURCE
RUN set -xe\
 && rpm -ivh ${COPY_JDK_CONFIGS_SOURCE}

# 安装依赖
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/copy-jdk-configs.spec

# 构建
RUN set -xe\
 && rpmbuild -ba ~/rpmbuild/SPECS/copy-jdk-configs.spec

FROM scratch AS exporter
COPY --from=builder /home/mockbuild/rpmbuild/RPMS /RPMS
COPY --from=builder /home/mockbuild/rpmbuild/SRPMS /SRPMS
