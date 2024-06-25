#!/bin/bash

set -xe
zabbix_version=`grep Version: ~/rpmbuild/SPECS/zabbix.spec | awk -F '[\\\\t\\\\.]+' '{print $2"."$3}'`

case "${zabbix_version}" in
    "5.0")
        patch -d ~/rpmbuild/SPECS/ -p1 -i ~/patchs/withpgsql-5.0.patch
        patch -d ~/rpmbuild/SPECS/ -p1 -i ~/patchs/zabbix-spec-5.0.patch
        patch -d ~/rpmbuild/SOURCES/ -p1 -i ~/patchs/zabbix-java-gateway-init-5.0.patch
    ;;
    "6.0")
        patch -d ~/rpmbuild/SPECS/ -p1 -i ~/patchs/withpgsql-6.0.patch
        patch -d ~/rpmbuild/SPECS/ -p1 -i ~/patchs/zabbix-spec-6.0.patch
        patch -d ~/rpmbuild/SOURCES/ -p1 -i ~/patchs/zabbix-java-gateway-init-6.0.patch
    ;;
esac
