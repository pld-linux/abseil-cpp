#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Abseil - C++ common libraries
Summary(pl.UTF-8):	Abseil - wspólne biblioteki C++
Name:		abseil-cpp
Version:	20211102.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/abseil/abseil-cpp/releases
Source0:	https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bdca561519192543378b7cade101ec43
URL:		https://abseil.io/
BuildRequires:	cmake >= 3.8
BuildRequires:	libstdc++-devel >= 6:7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# refers to _ZN4absl12lts_2021110213cord_internal17cordz_next_sampleE non-function symb ol from libabsl_condz_functions
%define		skip_post_check_so	libabsl_cord.so.*

%description
Abseil is an open-source collection of C++ library code designed to
augment the C++ standard library. The Abseil library code is collected
from Google's own C++ code base, has been extensively tested and used
in production.

%description -l pl.UTF-8
Abseil to zbiór bibliotek C++ o otwartych źródłach, zaprojektowancych
jako uzupełnienie biblioteki standardowej C++. Kod bibliotek został
zebrany z własnego kodu C++ Google'a, obszernie przetestowany i jest
używany produkcyjnie.

%package devel
Summary:	Header files for Abseil libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Abseil
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for Abseil libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Abseil.

%package static
Summary:	Static Abseil libraries
Summary(pl.UTF-8):	Statyczne biblioteki Abseil
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Abseil libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Abseil.

%prep
%setup -q

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DABSL_PROPAGATE_CXX_STD=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_CXX_STANDARD=17

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	-DABSL_PROPAGATE_CXX_STD=ON \
	-DCMAKE_CXX_STANDARD=17

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS FAQ.md README.md
%attr(755,root,root) %{_libdir}/libabsl_*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libabsl_*.so
%{_includedir}/absl
%{_libdir}/cmake/absl
%{_pkgconfigdir}/absl_*.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libabsl_*.a
%endif
