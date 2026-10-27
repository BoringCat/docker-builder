
ARG CENTOS_RELEASE=7
FROM quay.io/centos/centos:${CENTOS_RELEASE} AS centos-env

ARG CENTOS_RELEASE=7
COPY --chown=root:root yum.repos.d/${CENTOS_RELEASE} /etc/yum.repos.d/

RUN --mount=type=cache,target=/var/cache,sharing=private set -xe\
 && yum --disablerepo=epel install -y '@Development Tools' rpmdevtools yum-utils sudo ca-certificates unzip wget curl vim epel-release\
 && groupadd mock\
 && useradd mockbuild -m -G mock\
 && echo "mockbuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mockbuild\
 && sudo -u mockbuild -i 'rpmdev-setuptree'

USER mockbuild
WORKDIR /home/mockbuild

FROM centos-env AS builder
COPY --chown=mockbuild:mock rpmbuild/ /home/mockbuild/rpmbuild/

ARG COMMIT_SHA=e949d4402f76b4bc9b7b114418faace882f0ef12
RUN --mount=type=cache,target=/var/cache,sharing=private set -xe\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/unixbench.spec\
 && spectool -d "commit_sha ${COMMIT_SHA}" -g -R ~/rpmbuild/SPECS/unixbench.spec

RUN set -xe\
 && cat ~/rpmbuild/SPECS/unixbench.spec\
 && rpmbuild -D "commit_sha ${COMMIT_SHA}" -ba ~/rpmbuild/SPECS/unixbench.spec

FROM scratch AS exporter
COPY --from=builder /home/mockbuild/rpmbuild/RPMS /RPMS
COPY --from=builder /home/mockbuild/rpmbuild/SRPMS /SRPMS
