%define target arm-none-eabi
%define gdb_datarootdir %{_datarootdir}/gdb-%{target}-%{version}

Name:		%{target}-gdb
Version:	7.6.2
Release:	6%{?dist}
Summary:	GDB for (remote) debugging ARM targets
Group:		Development/Debuggers
License:	GPLv3+
URL:		http://sources.redhat.com/gdb/
Source0:	http://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.bz2

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	texinfo
BuildRequires:	ncurses-devel
BuildRequires:	python-devel
BuildRequires:	texinfo-tex
BuildRequires:	expat-devel

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc gdb-%{version}/{COPYING?,COPYING?.LIB}

%{_bindir}/%{target}-*
%{_mandir}/man1/%{target}-*.1.gz
%dir %{_datarootdir}/gdb-%{target}-%{version}
%{_datarootdir}/gdb-%{target}-%{version}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gdb/jit-reader.h

%changelog
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
