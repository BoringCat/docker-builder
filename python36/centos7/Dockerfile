FROM quay.io/centos/centos:7 AS centos-env

SHELL [ "/bin/bash", "-xeuo", "pipefail", "-c" ]

COPY repos/ /etc/yum.repos.d/

RUN --mount=type=cache,target=/var/cache,sharing=private\
    yum install -y epel-release --disablerepo=epel\
 && yum install -y '@Development Tools' rpmdevtools sudo ca-certificates unzip wget curl vim epel-release\
 && groupadd mock\
 && useradd mockbuild -m -G mock\
 && echo "mockbuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mockbuild\
 && sudo -u mockbuild -i 'rpmdev-setuptree'

USER mockbuild
WORKDIR /home/mockbuild

FROM centos-env AS builder

# 安装依赖
ARG SOURCE_URL
RUN --mount=type=cache,target=/var/cache,sharing=private\
    rpm -ivh ${SOURCE_URL}

COPY patchs/ /home/mockbuild/rpmbuild/SOURCES/

RUN sed -i ~/rpmbuild/SPECS/python3.spec\
    -e '/New patches go here/iPatch612: 00612-hmacopenssl-openssl11.patch\n'\
    -e '/^%patch404/a%patch612 -p1'\
    -e '/^export.*openssl/s/openssl/openssl11/g'\
    -e '/^BuildRequires.*openssl-devel/aBuildRequires: openssl11-devel'\
    -e '/^%configure/ised -i "s/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g" $topdir/configure'\
    -e '/^Release: 21/s/21/22/g'\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/python3.spec
# sed修改
## 增加针对 hmacopenssl的补丁，使其兼容openssl1.1
### - /New patches go here/iPatch612: 00612-hmacopenssl-openssl11.patch\n
### - /^%patch404/a%patch612 -p1
## 修改openssl为1.1
### - /^export.*openssl/s/openssl/openssl11/g
### - /^BuildRequires.*openssl-devel/aBuildRequires: openssl11-devel 不能替换 openssl-devel，因为setup.py会去检查
### - /^%configure/ised -i "s/PKG_CONFIG openssl /PKG_CONFIG openssl11 /g" $topdir/configure
## 增加Release版本号
### - /^Release: 21/s/21/22/g

# 构建 python3.6
RUN --mount=type=cache,target=/var/cache,sharing=private\
    rpmbuild -ba --clean ~/rpmbuild/SPECS/python3.spec

FROM scratch AS exporter
COPY --from=builder /home/mockbuild/rpmbuild/RPMS /RPMS
COPY --from=builder /home/mockbuild/rpmbuild/SRPMS /SRPMS
