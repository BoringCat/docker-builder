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

# 安装依赖并构建 tcl
ARG TCL_SOURCE
RUN --mount=type=cache,target=/var/cache set -xe\
 && rpm -ivh ${TCL_SOURCE}\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/tcl.spec\
 && rpmbuild -ba ~/rpmbuild/SPECS/tcl.spec

# 安装依赖并构建 tk
ARG TK_SOURCE
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/tcl-*.el7.x86_64.rpm\
 && rpm -ivh ${TK_SOURCE}\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/tk.spec\
 && rpmbuild -ba ~/rpmbuild/SPECS/tk.spec

FROM scratch AS exporter
COPY --from=builder /home/mockbuild/rpmbuild/RPMS /RPMS
COPY --from=builder /home/mockbuild/rpmbuild/SRPMS /SRPMS
