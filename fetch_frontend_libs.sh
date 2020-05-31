#!/bin/sh
set -ex

JQUERY_VERSION=3.5.1
BOOTSTRAP_VERSION=4.4.1
INTER_VERSION=3.13
VUE_VERSION=2.6.11
AXIOS_VERSION=0.19.2

wget https://cdn.jsdelivr.net/npm/jquery@${JQUERY_VERSION}/dist/jquery.min.js -O static/js/jquery.min.js
wget https://cdn.jsdelivr.net/npm/vue@${VUE_VERSION}/dist/vue.min.js -O static/js/vue.min.js
wget https://cdn.jsdelivr.net/npm/axios@${AXIOS_VERSION}/dist/axios.min.js -O static/js/axios.min.js
wget https://cdn.jsdelivr.net/npm/bootstrap@${BOOTSTRAP_VERSION}/dist/js/bootstrap.bundle.min.js -O static/js/bootstrap.bundle.min.js
mkdir -p /tmp/inter static/fonts
cd /tmp/inter && wget https://github.com/rsms/inter/releases/download/v${INTER_VERSION}/Inter-${INTER_VERSION}.zip
unzip Inter-${INTER_VERSION}.zip
cd -
mv /tmp/inter/Inter\ Web/* static/fonts/
rm -rf /tmp/inter

