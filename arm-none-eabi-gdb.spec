%define target arm-none-eabi
%define gdb_datarootdir %{_datarootdir}/gdb-%{target}-%{version}

Name:		%{target}-gdb
Version:	14.2
Release:	1%{?dist}
Summary:	GDB for (remote) debugging ARM targets
Group:		Development/Debuggers
License:	GPLv3+
URL:		https://sourceware.org/gdb/
Source0:	https://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.xz
Source1:	https://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.xz.sig
Source2:	gnu-keyring.gpg

BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  gnupg2
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
BuildRequires:  texinfo
BuildRequires:  texinfo-tex

%description
This is a version of GDB, the GNU Project debugger, for (remote)
debugging %{target} binaries. GDB allows you to see and modify what is
going on inside another program while it is executing.

%package devel
Summary: GDB for (remote) debugging ARM targets
Group: Development/Debuggers
Requires: %{name} = %{version}-%{release}

%description devel
This is a version of GDB, the GNU Project debugger, for (remote)
debugging %{target} binaries.  GDB allows you to see and modify what is
going on inside another program while it is executing.  This package
contains development headers for working with gdb.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q -c -n %{name}
cd gdb-%{version}

%build
mkdir -p build
cd build
# Set datarootdir to have target and version in so that we can exist
# side-by-side with other gdb installations of different versions
CFLAGS="$RPM_OPT_FLAGS" ../gdb-%{version}/configure --prefix=%{_prefix} \
	--libdir=%{_libdir} --mandir=%{_mandir} --infodir=%{_infodir} \
	--datarootdir=%{gdb_datarootdir} --disable-rpath \
	--target=%{target} --disable-nls --disable-werror --with-python --without-doc --with-xml --with-expat
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

# we don't want these as this is a cross-compiler
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# Get rid of the shared lib
rm -f $RPM_BUILD_ROOT%{_libdir}/lib%{target}-sim.a

# Non-linux targets don't have syscalls
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/gdb/syscalls

%files
%doc gdb-%{version}/{COPYING?,COPYING?.LIB}

%{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*.1.gz
%{_mandir}/man5/%{target}-*.5.gz
%dir %{_datarootdir}/gdb-%{target}-%{version}
%{_datarootdir}/gdb-%{target}-%{version}/*

%files devel
%{_includedir}/gdb/jit-reader.h
%{_includedir}/sim/callback.h
%{_includedir}/sim/sim.h

%changelog
* Sun May 20 2024 Raphael Lehmann <raphael+fedora@rleh.de> - 14.2-1
- Update to 14.2

* Sat Dec 16 2023 Raphael Lehmann <raphael+fedora@rleh.de> - 14.1-1
- Update to 14.1

* Sun Mar 12 2023 Raphael Lehmann <raphael+fedora@rleh.de> - 13.1-11
- Update to 13.1

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Iryna Shcherbina <ishcherb@redhat.com> - 7.6.2-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jérôme Glisse <jglisse@redhat.com> 7.6.2-1
- Drop texinfo patch, update to 7.6.2, fix rpath and other rpmlint warnings and errors.

* Fri Feb 7 2014 Maroš Zaťko <mzatko@fedoraproject.org> 7.4.1-2
- Add patch to fix texinfo build error

* Sun Oct 06 2013 David Lanzendörfer <david.lanzendoerfer@o2s.ch> 7.4.1-1
- Initial release
