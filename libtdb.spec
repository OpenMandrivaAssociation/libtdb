%define	major 1
%define libname	%mklibname tdb %{major}

Summary:	TDB is a Trivial Database
Name:		libtdb
Version:	1.0.6
Release:	%mkrel 8
License:	GPL
Group:		System/Libraries
URL:		http://sourceforge.net/projects/tdb
Source0:	tdb-%{version}.tar.bz2
Patch0:		tdb-1.0.6-strings.patch
# http://sourceforge.net/tracker/index.php?func=detail&aid=646773&group_id=9569&atid=309569
Patch1:		tdb-1.0.6-646773.diff
BuildRequires:	gdbm-devel
BuildRequires:	autoconf2.5
BuildRequires:	libtool
BuildRequires:	chrpath
BuildRoot:	%{_tmppath}/%{name}-buildroot

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

%package -n	%{libname}-devel
Summary:	Headers files of libtdb library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libtdb-devel = %{version}-%{release}

%description -n	%{libname}-devel
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
%patch0 -p0
%patch1 -p1

%build

%configure2_5x

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# install extras
install -m755 tdbiterate %{buildroot}%{_bindir}/
install -m755 tdbspeed %{buildroot}%{_bindir}/
install -m755 tdbtest %{buildroot}%{_bindir}/
install -m755 tdbtorture %{buildroot}%{_bindir}/

# nuke rpath
chrpath -d %{buildroot}%{_bindir}/tdbdump
chrpath -d %{buildroot}%{_bindir}/tdbtool

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr (-,root,root)
%doc AUTHORS ChangeLog INSTALL NEWS README TODO
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr (-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*.h
%{_mandir}/man3/tdb*

%files -n tdb-utils
%defattr (-,root,root)
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbiterate
%{_bindir}/tdbspeed
%{_bindir}/tdbtest
%{_bindir}/tdbtorture


