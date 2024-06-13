
ARG CENTOS_RELEASE
FROM quay.io/centos/centos:${CENTOS_RELEASE} as centos-env

RUN --mount=type=cache,target=/var/cache set -xe\
 && yum install -y '@Development Tools' rpmdevtools yum-utils sudo ca-certificates unzip wget curl vim epel-release\
 && groupadd mock\
 && useradd mockbuild -m -G mock\
 && echo "mockbuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mockbuild\
 && sudo -u mockbuild -i 'rpmdev-setuptree'

USER mockbuild
WORKDIR /home/mockbuild

FROM centos-env as builder
COPY --chown=mockbuild:mock rpmbuild/ /home/mockbuild/rpmbuild/

ARG COMMIT_SHA=a07fcc03264915c624f0e4818993c5b4df3fa703
RUN --mount=type=cache,target=/var/cache set -xe\
 && sudo yum-builddep -y ~/rpmbuild/SPECS/unixbench.spec\
 && spectool -d "commit_sha ${COMMIT_SHA}" -g -R ~/rpmbuild/SPECS/unixbench.spec

RUN set -xe\
 && cat ~/rpmbuild/SPECS/unixbench.spec\
 && rpmbuild -D "commit_sha ${COMMIT_SHA}" -ba ~/rpmbuild/SPECS/unixbench.spec

FROM scratch AS exporter
COPY --from=builder /home/mockbuild/rpmbuild/RPMS /RPMS
COPY --from=builder /home/mockbuild/rpmbuild/SRPMS /SRPMS
