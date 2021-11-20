#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Abseil - C++ common libraries
Summary(pl.UTF-8):	Abseil - wspólne biblioteki C++
Name:		abseil-cpp
Version:	20200923.3
Release:	2
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/abseil/abseil-cpp/releases
Source0:	https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	daba6e99c7a84e2242a0107bbd873669
URL:		https://abseil.io/
BuildRequires:	cmake >= 3.5
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	libstdc++-devel >= 6:4.7

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
	-DBUILD_SHARED_LIBS=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake ..

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
%attr(755,root,root) %{_libdir}/libabsl_bad_any_cast_impl.so
%attr(755,root,root) %{_libdir}/libabsl_bad_optional_access.so
%attr(755,root,root) %{_libdir}/libabsl_bad_variant_access.so
%attr(755,root,root) %{_libdir}/libabsl_base.so
%attr(755,root,root) %{_libdir}/libabsl_city.so
%attr(755,root,root) %{_libdir}/libabsl_civil_time.so
%attr(755,root,root) %{_libdir}/libabsl_cord.so
%attr(755,root,root) %{_libdir}/libabsl_debugging_internal.so
%attr(755,root,root) %{_libdir}/libabsl_demangle_internal.so
%attr(755,root,root) %{_libdir}/libabsl_examine_stack.so
%attr(755,root,root) %{_libdir}/libabsl_exponential_biased.so
%attr(755,root,root) %{_libdir}/libabsl_failure_signal_handler.so
%attr(755,root,root) %{_libdir}/libabsl_flags.so
%attr(755,root,root) %{_libdir}/libabsl_flags_commandlineflag.so
%attr(755,root,root) %{_libdir}/libabsl_flags_commandlineflag_internal.so
%attr(755,root,root) %{_libdir}/libabsl_flags_config.so
%attr(755,root,root) %{_libdir}/libabsl_flags_internal.so
%attr(755,root,root) %{_libdir}/libabsl_flags_marshalling.so
%attr(755,root,root) %{_libdir}/libabsl_flags_parse.so
%attr(755,root,root) %{_libdir}/libabsl_flags_private_handle_accessor.so
%attr(755,root,root) %{_libdir}/libabsl_flags_program_name.so
%attr(755,root,root) %{_libdir}/libabsl_flags_reflection.so
%attr(755,root,root) %{_libdir}/libabsl_flags_usage.so
%attr(755,root,root) %{_libdir}/libabsl_flags_usage_internal.so
%attr(755,root,root) %{_libdir}/libabsl_graphcycles_internal.so
%attr(755,root,root) %{_libdir}/libabsl_hash.so
%attr(755,root,root) %{_libdir}/libabsl_hashtablez_sampler.so
%attr(755,root,root) %{_libdir}/libabsl_int128.so
%attr(755,root,root) %{_libdir}/libabsl_leak_check.so
%attr(755,root,root) %{_libdir}/libabsl_leak_check_disable.so
%attr(755,root,root) %{_libdir}/libabsl_log_severity.so
%attr(755,root,root) %{_libdir}/libabsl_malloc_internal.so
%attr(755,root,root) %{_libdir}/libabsl_periodic_sampler.so
%attr(755,root,root) %{_libdir}/libabsl_random_distributions.so
%attr(755,root,root) %{_libdir}/libabsl_random_internal_distribution_test_util.so
%attr(755,root,root) %{_libdir}/libabsl_random_internal_platform.so
%attr(755,root,root) %{_libdir}/libabsl_random_internal_pool_urbg.so
%attr(755,root,root) %{_libdir}/libabsl_random_internal_randen.so
%attr(755,root,root) %{_libdir}/libabsl_random_internal_randen_hwaes.so
%attr(755,root,root) %{_libdir}/libabsl_random_internal_randen_hwaes_impl.so
%attr(755,root,root) %{_libdir}/libabsl_random_internal_randen_slow.so
%attr(755,root,root) %{_libdir}/libabsl_random_internal_seed_material.so
%attr(755,root,root) %{_libdir}/libabsl_random_seed_gen_exception.so
%attr(755,root,root) %{_libdir}/libabsl_random_seed_sequences.so
%attr(755,root,root) %{_libdir}/libabsl_raw_hash_set.so
%attr(755,root,root) %{_libdir}/libabsl_raw_logging_internal.so
%attr(755,root,root) %{_libdir}/libabsl_scoped_set_env.so
%attr(755,root,root) %{_libdir}/libabsl_spinlock_wait.so
%attr(755,root,root) %{_libdir}/libabsl_stacktrace.so
%attr(755,root,root) %{_libdir}/libabsl_status.so
%attr(755,root,root) %{_libdir}/libabsl_statusor.so
%attr(755,root,root) %{_libdir}/libabsl_str_format_internal.so
%attr(755,root,root) %{_libdir}/libabsl_strerror.so
%attr(755,root,root) %{_libdir}/libabsl_strings.so
%attr(755,root,root) %{_libdir}/libabsl_strings_internal.so
%attr(755,root,root) %{_libdir}/libabsl_symbolize.so
%attr(755,root,root) %{_libdir}/libabsl_synchronization.so
%attr(755,root,root) %{_libdir}/libabsl_throw_delegate.so
%attr(755,root,root) %{_libdir}/libabsl_time.so
%attr(755,root,root) %{_libdir}/libabsl_time_zone.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/absl
%{_libdir}/cmake/absl

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libabsl_bad_any_cast_impl.a
%{_libdir}/libabsl_bad_optional_access.a
%{_libdir}/libabsl_bad_variant_access.a
%{_libdir}/libabsl_base.a
%{_libdir}/libabsl_city.a
%{_libdir}/libabsl_civil_time.a
%{_libdir}/libabsl_cord.a
%{_libdir}/libabsl_debugging_internal.a
%{_libdir}/libabsl_demangle_internal.a
%{_libdir}/libabsl_examine_stack.a
%{_libdir}/libabsl_exponential_biased.a
%{_libdir}/libabsl_failure_signal_handler.a
%{_libdir}/libabsl_flags.a
%{_libdir}/libabsl_flags_commandlineflag.a
%{_libdir}/libabsl_flags_commandlineflag_internal.a
%{_libdir}/libabsl_flags_config.a
%{_libdir}/libabsl_flags_internal.a
%{_libdir}/libabsl_flags_marshalling.a
%{_libdir}/libabsl_flags_parse.a
%{_libdir}/libabsl_flags_private_handle_accessor.a
%{_libdir}/libabsl_flags_program_name.a
%{_libdir}/libabsl_flags_reflection.a
%{_libdir}/libabsl_flags_usage.a
%{_libdir}/libabsl_flags_usage_internal.a
%{_libdir}/libabsl_graphcycles_internal.a
%{_libdir}/libabsl_hash.a
%{_libdir}/libabsl_hashtablez_sampler.a
%{_libdir}/libabsl_int128.a
%{_libdir}/libabsl_leak_check.a
%{_libdir}/libabsl_leak_check_disable.a
%{_libdir}/libabsl_log_severity.a
%{_libdir}/libabsl_malloc_internal.a
%{_libdir}/libabsl_periodic_sampler.a
%{_libdir}/libabsl_random_distributions.a
%{_libdir}/libabsl_random_internal_distribution_test_util.a
%{_libdir}/libabsl_random_internal_platform.a
%{_libdir}/libabsl_random_internal_pool_urbg.a
%{_libdir}/libabsl_random_internal_randen.a
%{_libdir}/libabsl_random_internal_randen_hwaes.a
%{_libdir}/libabsl_random_internal_randen_hwaes_impl.a
%{_libdir}/libabsl_random_internal_randen_slow.a
%{_libdir}/libabsl_random_internal_seed_material.a
%{_libdir}/libabsl_random_seed_gen_exception.a
%{_libdir}/libabsl_random_seed_sequences.a
%{_libdir}/libabsl_raw_hash_set.a
%{_libdir}/libabsl_raw_logging_internal.a
%{_libdir}/libabsl_scoped_set_env.a
%{_libdir}/libabsl_spinlock_wait.a
%{_libdir}/libabsl_stacktrace.a
%{_libdir}/libabsl_status.a
%{_libdir}/libabsl_statusor.a
%{_libdir}/libabsl_str_format_internal.a
%{_libdir}/libabsl_strerror.a
%{_libdir}/libabsl_strings.a
%{_libdir}/libabsl_strings_internal.a
%{_libdir}/libabsl_symbolize.a
%{_libdir}/libabsl_synchronization.a
%{_libdir}/libabsl_throw_delegate.a
%{_libdir}/libabsl_time.a
%{_libdir}/libabsl_time_zone.a
%endif
