# Fedora Package `arm-none-eabi-gdb`

https://copr.fedorainfracloud.org/coprs/rleh/arm-none-eabi-gdb/


## How-To build local

Build podman/docker image:
```sh
podman build --tag fedora-rpmbuild:43 --file Dockerfile
```

Run podman/docker image with spec file and SOURCES/ directory mounted:
```sh
podman run --rm -v ./SOURCES/:/root/rpmbuild/SOURCES/:z -v ./arm-none-eabi-gdb.spec:/root/rpmbuild/SPECS/arm-none-eabi-gdb.spec:ro,z -it fedora-rpmbuild:43
```

Install build dependencies and build (from container shell):
```sh
cd
dnf builddep rpmbuild/SPECS/arm-none-eabi-gdb.spec
rpmbuild --undefine=_disable_source_fetch -ba rpmbuild/SPECS/arm-none-eabi-gdb.spec
```
