FROM fedora:43
LABEL maintainer="Raphael Lehmann <raphael+docker@rleh.de>"
LABEL Description="Image for building Fedora packages"
LABEL org.opencontainers.image.source https://github.com/rleh/fedora-arm-none-eabi-gdb

RUN dnf install -y rpmdevtools dnf-plugins-core && dnf clean all && rpmdev-setuptree
RUN dnf install -y expat-devel gcc gcc-c++ gmp-devel mpfr-devel gnupg2 ncurses-devel python3-devel texinfo texinfo-tex && dnf clean all
