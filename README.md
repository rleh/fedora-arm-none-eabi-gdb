# Fedora Package `arm-none-eabi-gdb`

https://copr.fedorainfracloud.org/coprs/rleh/arm-none-eabi-gdb/


## How-To build local

Using Docker/Podman:
```sh
podman run --rm -it fedora:43
```
Inside the container shell:
```sh
dnf install -y rpmdevtools dnf-plugins-core
rpmdev-setuptree
```

On your machine, copy the Spec file and keyring into the container:
```sh
podman cp arm-none-eabi-gdb.spec {container_name}:/root/rpmbuild/SPECS/
podman cp gnu-keyring.gpg {container_name}:/root/rpmbuild/SOURCES/
```

Install build dependencies and build (from container shell):
```sh
cd
dnf builddep rpmbuild/SPECS/arm-none-eabi-gdb.spec
rpmbuild --undefine=_disable_source_fetch -ba rpmbuild/SPECS/arm-none-eabi-gdb.spec
```
