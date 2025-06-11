Name:           osmo-iuh
Version:        1.7.0
Release:        1.dcbw%{?dist}
Summary:        Osmocom 3GPP Iuh interface
License:        AGPL-3.0-or-later AND GPL-2.0-only

URL:            https://osmocom.org/projects/osmohnbgw/wiki

BuildRequires:  git gcc autoconf automake libtool python3 doxygen
BuildRequires:  lksctp-tools-devel
BuildRequires:  libasn1c-devel >= 0.9.38
BuildRequires:  libosmocore-devel >= 1.10.0
BuildRequires:  libosmo-netif-devel >= 1.6.0
BuildRequires:  libosmo-sigtran-devel >= 2.1.1

Source0: %{name}-%{version}.tar.bz2

%description
C-language implementation of the 3GPP Iuh interface.

%package          devel
Summary:          Development files for %{name}
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description      devel
Development files for %{name}.


%prep
%autosetup -p1


%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
echo "%{version}" >.tarball-version
autoreconf -fiv
%configure --enable-shared \
           --disable-static

# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} \;
sed -i -e 's|UNKNOWN|%{version}|g' %{buildroot}/%{_libdir}/pkgconfig/*.pc


%check
make check


%ldconfig_scriptlets


%files
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/osmocom/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 1.7.0
- Update to 1.7.0

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- git update releases
