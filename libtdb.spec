%define	major 1
%define libname %mklibname tdb %{major}
%define develname %mklibname tdb -d
%define	svn	20071206

Summary:	TDB is a Trivial Database
Name:		libtdb
Version:	1.1.1
Release:	%mkrel 0.%{svn}.1
License:	GPL
Group:		System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://sourceforge.net/projects/tdb
Source0:	tdb-%{version}-svn%{svn}.tar.lzma
Patch0:		tdb-1.1.1-add-missing-headers.patch
BuildRequires:	gdbm-devel
BuildRequires:	autoconf2.5
BuildRequires:	libtool

%description
TDB is a Trivial Database. In concept, it is very much like GDBM, 
and BSD's DB except that it allows multiple simultaneous writers 
and uses locking internally to keep writers from trampling on 
each other. TDB is also extremely small.

%package -n	%{libname}
Summary:	TDB is a Trivial Database
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
TDB is a Trivial Database. In concept, it is very much like GDBM,
and BSD's DB except that it allows multiple simultaneous writers 
and uses locking internally to keep writers from trampling on each
other. TDB is also extremely small.

%package -n	%{develname}
Summary:	Headers files of libtdb library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libtdb-devel = %{version}-%{release}
Obsoletes:	%{mklibname tdb 1 -d}

%description -n	%{develname}
TDB is a Trivial Database. In concept, it is very much like GDBM,
and BSD's DB except that it allows multiple simultaneous writers
and uses locking internally to keep writers from trampling on each
other. TDB is also extremely small.

%package -n	tdb-utils
Summary:	Utilities using the %{libname} library
Group:		Databases
Requires:	%{libname} = %{version}
Conflicts:	samba-common

%description -n	tdb-utils
Utilities using the %{libname} library.

%prep
%setup -q -n tdb-%{version}
%patch0 -p1 -b .addheader

%build
./autogen.sh
%configure2_5x
%make all bin/tdbtest bin/tdbtorture

%install
rm -rf %{buildroot}

%makeinstall_std
ln -s libtdb.so.%{major} %{buildroot}%{_libdir}/libtdb.so
# install extras
install -m755 bin/tdbtest %{buildroot}%{_bindir}/
install -m755 bin/tdbtorture %{buildroot}%{_bindir}/

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr (-,root,root)
%doc docs/README
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr (-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-utils
%defattr (-,root,root)
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbbackup
%{_bindir}/tdbtest
%{_bindir}/tdbtorture
