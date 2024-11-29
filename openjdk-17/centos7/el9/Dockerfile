
FROM quay.io/centos/centos:stream9 AS spec-generator
RUN --mount=type=cache,target=/var/cache set -xe\
 && dnf install -y rpmdevtools wget\
 && groupadd mock\
 && useradd mockbuild -m -G mock

USER mockbuild
WORKDIR /home/mockbuild

ARG OPENJDK_SOURCE
ARG OPENJDK_FILE
RUN set -xe\
 && rpmdev-setuptree\
 && wget -q ${OPENJDK_SOURCE} -O /tmp/${OPENJDK_FILE}\
 && rpm -ivh /tmp/${OPENJDK_FILE}\
 && rpmspec -D 'dist .el7'\
    --without slowdebug\
    --without fastdebug\
    --without system_libs\
    -P ~/rpmbuild/SPECS/java-17-openjdk.spec\
 | sed -e '/Recommends:/d'\
       -e '/Suggests:/d'\
       -e '/: crypto-policies/d'\
       -e '/BuildRequires: java-17/d'\
       -e '/%package debug/,/^$/d'\
       -e '/# Check system crypto/,/^$/d'\
       -e 's~-specs=\S*-annobin-\w*~~g'\
 > /tmp/java-17-openjdk.spec
# sed修改
## /Recommends:/d;/Suggests:/d: centos7 的 rpm-build 不支持这两个标签
## /: crypto-policies/d: centos7 没有 crypto-policies 包
## /BuildRequires: java-17/d: 使用 java/GA/jdk17.0.2 作为 bootjdk，因此不需要编译依赖 java-17
## /# Check system crypto/,/^$/d: 去掉了 crypto-policies，所以也去掉测试用例
## /%package debug/,/^$/d: centos7 的 rpm-build 默认就有 debuginfo 配置
## s~-specs=\S*-annobin-\w*~~g: centos7 的 redhat-rpm-config 没有 annobin

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

# 安装 gcc-11
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo yum install -y centos-release-scl.noarch centos-release-scl-rh.noarch\
 && sudo yum install -y devtoolset-11-gcc-c++ libstdc++-static redhat-rpm-config

# 下载 bootjdk
ARG BOOTJDK_SOURCE
ARG BOOTJDK_FILE
ARG BOOTJDK_DIR
RUN set -xe\
 && wget -q ${BOOTJDK_SOURCE} -O ${BOOTJDK_FILE}\
 && sudo mkdir -p /usr/lib/jvm\
 && cd /usr/lib/jvm\
 && sudo tar xf ~/${BOOTJDK_FILE}\
 && if [ "${BOOTJDK_DIR}" != "java-17-openjdk" ]; then sudo mv -v ${BOOTJDK_DIR} java-17-openjdk; fi

# 安装源码包
ARG OPENJDK_FILE
COPY --from=spec-generator --chown=mockbuild:mock /tmp /tmp
RUN set -xe\
 && rpm -ivh /tmp/${OPENJDK_FILE}\
 && mv /tmp/java-17-openjdk.spec ~/rpmbuild/SPECS/java-17-openjdk.spec

# 安装依赖
ARG JAVAPACKAGES_SOURCE
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo rpm -ivh ${JAVAPACKAGES_SOURCE}\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/java-17-openjdk.spec

# 构建（>30min）
RUN set -xe\
 && source /opt/rh/devtoolset-11/enable\
 && rpmbuild -ba ~/rpmbuild/SPECS/java-17-openjdk.spec

FROM scratch AS exporter
COPY --from=builder /home/mockbuild/rpmbuild/RPMS /RPMS
COPY --from=builder /home/mockbuild/rpmbuild/SRPMS /SRPMS
