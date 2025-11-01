#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	test_libs	# test libraries
#
Summary:	Abseil - C++ common libraries
Summary(pl.UTF-8):	Abseil - wspólne biblioteki C++
Name:		abseil-cpp
Version:	20250814.0
Release:	3
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/abseil/abseil-cpp/releases
Source0:	https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	016feacd6a6b3b9a47ab844e61f4f7bd
Patch0:		x32.patch
URL:		https://abseil.io/
BuildRequires:	cmake >= 3.16
BuildRequires:	gmock-devel
BuildRequires:	gtest-devel
%ifnarch %{arch_with_atomics64}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpmbuild(macros) >= 2.025
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# refers to _ZN4absl12lts_2021110213cord_internal17cordz_next_sampleE non-function symbol from libabsl_condz_functions
%define		skip_post_check_so	libabsl_cord.so.*

%define		abiver			2508.0.0

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
Requires:	gmock-devel
Requires:	gtest-devel
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

%package test
Summary:	Abseil C++ test libraries
Summary(pl.UTF-8):	Biblioteki testowe Abseil C++
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description test
Abseil C++ test libraries.

%description test -l pl.UTF-8
Biblioteki testowe Abseil C++.

%package test-devel
Summary:	Header files for Abseil C++ test libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek testowych Abseil C++
Group:		Development/Libraries
Requires:	%{name}-test = %{version}-%{release}

%description test-devel
Header files for Abseil C++ test libraries.

%description test-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek testowych Abseil C++.

%package test-static
Summary:	Static Abseil C++ test libraries
Summary(pl.UTF-8):	Statyczne biblioteki testowe Abseil C++
Group:		Development/Libraries
Requires:	%{name}-test-devel = %{version}-%{release}

%description test-static
Static Abseil C++ test libraries.

%description test-static -l pl.UTF-8
Statyczne biblioteki testowe Abseil C++.

%prep
%setup -q
%patch -P0 -p1

%build
%if %{with static_libs}
%cmake -B build-static \
	-DABSL_PROPAGATE_CXX_STD=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_CXX_STANDARD=17 \
	-DABSL_USE_EXTERNAL_GOOGLETEST:BOOL=ON \
	-DABSL_FIND_GOOGLETEST:BOOL=ON \
	-DABSL_BUILD_TESTING:BOOL=%{__ON_OFF test_libs} \
	-DABSL_BUILD_TEST_HELPERS:BOOL=%{__ON_OFF test_libs}

%{__make} -C build-static
%endif

%cmake -B build \
	-DABSL_PROPAGATE_CXX_STD:BOOL=ON \
	-DCMAKE_CXX_STANDARD:STRING=17 \
	-DABSL_USE_EXTERNAL_GOOGLETEST:BOOL=ON \
	-DABSL_FIND_GOOGLETEST:BOOL=ON \
	-DABSL_BUILD_TESTING:BOOL=%{__ON_OFF test_libs} \
	-DABSL_BUILD_TEST_HELPERS:BOOL=%{__ON_OFF test_libs} \
%ifnarch %{arch_with_atomics64}
	-DCMAKE_CXX_STANDARD_LIBRARIES="-latomic"
%endif

%{__make} -C build

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

%post	test -p /sbin/ldconfig
%postun	test -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS FAQ.md README.md
%{_libdir}/libabsl_base.so.%{abiver}
%{_libdir}/libabsl_city.so.%{abiver}
%{_libdir}/libabsl_civil_time.so.%{abiver}
%{_libdir}/libabsl_cord_internal.so.%{abiver}
%{_libdir}/libabsl_cord.so.%{abiver}
%{_libdir}/libabsl_cordz_functions.so.%{abiver}
%{_libdir}/libabsl_cordz_handle.so.%{abiver}
%{_libdir}/libabsl_cordz_info.so.%{abiver}
%{_libdir}/libabsl_cordz_sample_token.so.%{abiver}
%{_libdir}/libabsl_crc32c.so.%{abiver}
%{_libdir}/libabsl_crc_cord_state.so.%{abiver}
%{_libdir}/libabsl_crc_cpu_detect.so.%{abiver}
%{_libdir}/libabsl_crc_internal.so.%{abiver}
%{_libdir}/libabsl_debugging_internal.so.%{abiver}
%{_libdir}/libabsl_decode_rust_punycode.so.%{abiver}
%{_libdir}/libabsl_demangle_internal.so.%{abiver}
%{_libdir}/libabsl_demangle_rust.so.%{abiver}
%{_libdir}/libabsl_die_if_null.so.%{abiver}
%{_libdir}/libabsl_examine_stack.so.%{abiver}
%{_libdir}/libabsl_exponential_biased.so.%{abiver}
%{_libdir}/libabsl_failure_signal_handler.so.%{abiver}
%{_libdir}/libabsl_flags_commandlineflag_internal.so.%{abiver}
%{_libdir}/libabsl_flags_commandlineflag.so.%{abiver}
%{_libdir}/libabsl_flags_config.so.%{abiver}
%{_libdir}/libabsl_flags_internal.so.%{abiver}
%{_libdir}/libabsl_flags_marshalling.so.%{abiver}
%{_libdir}/libabsl_flags_parse.so.%{abiver}
%{_libdir}/libabsl_flags_private_handle_accessor.so.%{abiver}
%{_libdir}/libabsl_flags_program_name.so.%{abiver}
%{_libdir}/libabsl_flags_reflection.so.%{abiver}
%{_libdir}/libabsl_flags_usage_internal.so.%{abiver}
%{_libdir}/libabsl_flags_usage.so.%{abiver}
%{_libdir}/libabsl_graphcycles_internal.so.%{abiver}
%{_libdir}/libabsl_hash.so.%{abiver}
%{_libdir}/libabsl_hashtable_profiler.so.%{abiver}
%{_libdir}/libabsl_hashtablez_sampler.so.%{abiver}
%{_libdir}/libabsl_int128.so.%{abiver}
%{_libdir}/libabsl_kernel_timeout_internal.so.%{abiver}
%{_libdir}/libabsl_leak_check.so.%{abiver}
%{_libdir}/libabsl_log_entry.so.%{abiver}
%{_libdir}/libabsl_log_flags.so.%{abiver}
%{_libdir}/libabsl_log_globals.so.%{abiver}
%{_libdir}/libabsl_log_initialize.so.%{abiver}
%{_libdir}/libabsl_log_internal_check_op.so.%{abiver}
%{_libdir}/libabsl_log_internal_conditions.so.%{abiver}
%{_libdir}/libabsl_log_internal_fnmatch.so.%{abiver}
%{_libdir}/libabsl_log_internal_format.so.%{abiver}
%{_libdir}/libabsl_log_internal_globals.so.%{abiver}
%{_libdir}/libabsl_log_internal_log_sink_set.so.%{abiver}
%{_libdir}/libabsl_log_internal_message.so.%{abiver}
%{_libdir}/libabsl_log_internal_nullguard.so.%{abiver}
%{_libdir}/libabsl_log_internal_proto.so.%{abiver}
%{_libdir}/libabsl_log_internal_structured_proto.so.%{abiver}
%{_libdir}/libabsl_log_severity.so.%{abiver}
%{_libdir}/libabsl_log_sink.so.%{abiver}
%{_libdir}/libabsl_malloc_internal.so.%{abiver}
%{_libdir}/libabsl_periodic_sampler.so.%{abiver}
%{_libdir}/libabsl_poison.so.%{abiver}
%{_libdir}/libabsl_profile_builder.so.%{abiver}
%{_libdir}/libabsl_random_distributions.so.%{abiver}
%{_libdir}/libabsl_random_internal_distribution_test_util.so.%{abiver}
%{_libdir}/libabsl_random_internal_entropy_pool.so.%{abiver}
%{_libdir}/libabsl_random_internal_platform.so.%{abiver}
%{_libdir}/libabsl_random_internal_randen_hwaes_impl.so.%{abiver}
%{_libdir}/libabsl_random_internal_randen_hwaes.so.%{abiver}
%{_libdir}/libabsl_random_internal_randen_slow.so.%{abiver}
%{_libdir}/libabsl_random_internal_randen.so.%{abiver}
%{_libdir}/libabsl_random_internal_seed_material.so.%{abiver}
%{_libdir}/libabsl_random_seed_gen_exception.so.%{abiver}
%{_libdir}/libabsl_random_seed_sequences.so.%{abiver}
%{_libdir}/libabsl_raw_hash_set.so.%{abiver}
%{_libdir}/libabsl_raw_logging_internal.so.%{abiver}
%{_libdir}/libabsl_scoped_set_env.so.%{abiver}
%{_libdir}/libabsl_spinlock_wait.so.%{abiver}
%{_libdir}/libabsl_stacktrace.so.%{abiver}
%{_libdir}/libabsl_statusor.so.%{abiver}
%{_libdir}/libabsl_status.so.%{abiver}
%{_libdir}/libabsl_strerror.so.%{abiver}
%{_libdir}/libabsl_str_format_internal.so.%{abiver}
%{_libdir}/libabsl_strings_internal.so.%{abiver}
%{_libdir}/libabsl_strings.so.%{abiver}
%{_libdir}/libabsl_string_view.so.%{abiver}
%{_libdir}/libabsl_symbolize.so.%{abiver}
%{_libdir}/libabsl_synchronization.so.%{abiver}
%{_libdir}/libabsl_throw_delegate.so.%{abiver}
%{_libdir}/libabsl_time.so.%{abiver}
%{_libdir}/libabsl_time_zone.so.%{abiver}
%{_libdir}/libabsl_tracing_internal.so.%{abiver}
%{_libdir}/libabsl_utf8_for_code_point.so.%{abiver}
%{_libdir}/libabsl_vlog_config_internal.so.%{abiver}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libabsl_base.so
%{_libdir}/libabsl_city.so
%{_libdir}/libabsl_civil_time.so
%{_libdir}/libabsl_cord_internal.so
%{_libdir}/libabsl_cord.so
%{_libdir}/libabsl_cordz_functions.so
%{_libdir}/libabsl_cordz_handle.so
%{_libdir}/libabsl_cordz_info.so
%{_libdir}/libabsl_cordz_sample_token.so
%{_libdir}/libabsl_crc32c.so
%{_libdir}/libabsl_crc_cord_state.so
%{_libdir}/libabsl_crc_cpu_detect.so
%{_libdir}/libabsl_crc_internal.so
%{_libdir}/libabsl_debugging_internal.so
%{_libdir}/libabsl_decode_rust_punycode.so
%{_libdir}/libabsl_demangle_internal.so
%{_libdir}/libabsl_demangle_rust.so
%{_libdir}/libabsl_die_if_null.so
%{_libdir}/libabsl_examine_stack.so
%{_libdir}/libabsl_exponential_biased.so
%{_libdir}/libabsl_failure_signal_handler.so
%{_libdir}/libabsl_flags_commandlineflag_internal.so
%{_libdir}/libabsl_flags_commandlineflag.so
%{_libdir}/libabsl_flags_config.so
%{_libdir}/libabsl_flags_internal.so
%{_libdir}/libabsl_flags_marshalling.so
%{_libdir}/libabsl_flags_parse.so
%{_libdir}/libabsl_flags_private_handle_accessor.so
%{_libdir}/libabsl_flags_program_name.so
%{_libdir}/libabsl_flags_reflection.so
%{_libdir}/libabsl_flags_usage_internal.so
%{_libdir}/libabsl_flags_usage.so
%{_libdir}/libabsl_graphcycles_internal.so
%{_libdir}/libabsl_hash.so
%{_libdir}/libabsl_hashtable_profiler.so
%{_libdir}/libabsl_hashtablez_sampler.so
%{_libdir}/libabsl_int128.so
%{_libdir}/libabsl_kernel_timeout_internal.so
%{_libdir}/libabsl_leak_check.so
%{_libdir}/libabsl_log_entry.so
%{_libdir}/libabsl_log_flags.so
%{_libdir}/libabsl_log_globals.so
%{_libdir}/libabsl_log_initialize.so
%{_libdir}/libabsl_log_internal_check_op.so
%{_libdir}/libabsl_log_internal_conditions.so
%{_libdir}/libabsl_log_internal_fnmatch.so
%{_libdir}/libabsl_log_internal_format.so
%{_libdir}/libabsl_log_internal_globals.so
%{_libdir}/libabsl_log_internal_log_sink_set.so
%{_libdir}/libabsl_log_internal_message.so
%{_libdir}/libabsl_log_internal_nullguard.so
%{_libdir}/libabsl_log_internal_proto.so
%{_libdir}/libabsl_log_internal_structured_proto.so
%{_libdir}/libabsl_log_severity.so
%{_libdir}/libabsl_log_sink.so
%{_libdir}/libabsl_malloc_internal.so
%{_libdir}/libabsl_periodic_sampler.so
%{_libdir}/libabsl_poison.so
%{_libdir}/libabsl_profile_builder.so
%{_libdir}/libabsl_random_distributions.so
%{_libdir}/libabsl_random_internal_distribution_test_util.so
%{_libdir}/libabsl_random_internal_entropy_pool.so
%{_libdir}/libabsl_random_internal_platform.so
%{_libdir}/libabsl_random_internal_randen_hwaes_impl.so
%{_libdir}/libabsl_random_internal_randen_hwaes.so
%{_libdir}/libabsl_random_internal_randen_slow.so
%{_libdir}/libabsl_random_internal_randen.so
%{_libdir}/libabsl_random_internal_seed_material.so
%{_libdir}/libabsl_random_seed_gen_exception.so
%{_libdir}/libabsl_random_seed_sequences.so
%{_libdir}/libabsl_raw_hash_set.so
%{_libdir}/libabsl_raw_logging_internal.so
%{_libdir}/libabsl_scoped_set_env.so
%{_libdir}/libabsl_spinlock_wait.so
%{_libdir}/libabsl_stacktrace.so
%{_libdir}/libabsl_statusor.so
%{_libdir}/libabsl_status.so
%{_libdir}/libabsl_strerror.so
%{_libdir}/libabsl_str_format_internal.so
%{_libdir}/libabsl_strings_internal.so
%{_libdir}/libabsl_strings.so
%{_libdir}/libabsl_string_view.so
%{_libdir}/libabsl_symbolize.so
%{_libdir}/libabsl_synchronization.so
%{_libdir}/libabsl_throw_delegate.so
%{_libdir}/libabsl_time.so
%{_libdir}/libabsl_time_zone.so
%{_libdir}/libabsl_tracing_internal.so
%{_libdir}/libabsl_utf8_for_code_point.so
%{_libdir}/libabsl_vlog_config_internal.so
%{_includedir}/absl
%{_libdir}/cmake/absl
%{_pkgconfigdir}/absl_absl_check.pc
%{_pkgconfigdir}/absl_absl_log.pc
%{_pkgconfigdir}/absl_absl_vlog_is_on.pc
%{_pkgconfigdir}/absl_algorithm.pc
%{_pkgconfigdir}/absl_algorithm_container.pc
%{_pkgconfigdir}/absl_any.pc
%{_pkgconfigdir}/absl_any_invocable.pc
%{_pkgconfigdir}/absl_atomic_hook.pc
%{_pkgconfigdir}/absl_bad_any_cast.pc
%{_pkgconfigdir}/absl_bad_optional_access.pc
%{_pkgconfigdir}/absl_bad_variant_access.pc
%{_pkgconfigdir}/absl_base.pc
%{_pkgconfigdir}/absl_base_internal.pc
%{_pkgconfigdir}/absl_bind_front.pc
%{_pkgconfigdir}/absl_bits.pc
%{_pkgconfigdir}/absl_bounded_utf8_length_sequence.pc
%{_pkgconfigdir}/absl_btree.pc
%{_pkgconfigdir}/absl_charset.pc
%{_pkgconfigdir}/absl_check.pc
%{_pkgconfigdir}/absl_city.pc
%{_pkgconfigdir}/absl_civil_time.pc
%{_pkgconfigdir}/absl_cleanup.pc
%{_pkgconfigdir}/absl_cleanup_internal.pc
%{_pkgconfigdir}/absl_common_policy_traits.pc
%{_pkgconfigdir}/absl_compare.pc
%{_pkgconfigdir}/absl_compressed_tuple.pc
%{_pkgconfigdir}/absl_config.pc
%{_pkgconfigdir}/absl_container_common.pc
%{_pkgconfigdir}/absl_container_memory.pc
%{_pkgconfigdir}/absl_cord.pc
%{_pkgconfigdir}/absl_cord_internal.pc
%{_pkgconfigdir}/absl_cordz_functions.pc
%{_pkgconfigdir}/absl_cordz_handle.pc
%{_pkgconfigdir}/absl_cordz_info.pc
%{_pkgconfigdir}/absl_cordz_sample_token.pc
%{_pkgconfigdir}/absl_cordz_statistics.pc
%{_pkgconfigdir}/absl_cordz_update_scope.pc
%{_pkgconfigdir}/absl_cordz_update_tracker.pc
%{_pkgconfigdir}/absl_core_headers.pc
%{_pkgconfigdir}/absl_crc32c.pc
%{_pkgconfigdir}/absl_crc_cord_state.pc
%{_pkgconfigdir}/absl_crc_cpu_detect.pc
%{_pkgconfigdir}/absl_crc_internal.pc
%{_pkgconfigdir}/absl_debugging.pc
%{_pkgconfigdir}/absl_debugging_internal.pc
%{_pkgconfigdir}/absl_decode_rust_punycode.pc
%{_pkgconfigdir}/absl_demangle_internal.pc
%{_pkgconfigdir}/absl_demangle_rust.pc
%{_pkgconfigdir}/absl_die_if_null.pc
%{_pkgconfigdir}/absl_dynamic_annotations.pc
%{_pkgconfigdir}/absl_endian.pc
%{_pkgconfigdir}/absl_errno_saver.pc
%{_pkgconfigdir}/absl_examine_stack.pc
%{_pkgconfigdir}/absl_exponential_biased.pc
%{_pkgconfigdir}/absl_failure_signal_handler.pc
%{_pkgconfigdir}/absl_fast_type_id.pc
%{_pkgconfigdir}/absl_fixed_array.pc
%{_pkgconfigdir}/absl_flags.pc
%{_pkgconfigdir}/absl_flags_commandlineflag.pc
%{_pkgconfigdir}/absl_flags_commandlineflag_internal.pc
%{_pkgconfigdir}/absl_flags_config.pc
%{_pkgconfigdir}/absl_flags_internal.pc
%{_pkgconfigdir}/absl_flags_marshalling.pc
%{_pkgconfigdir}/absl_flags_parse.pc
%{_pkgconfigdir}/absl_flags_path_util.pc
%{_pkgconfigdir}/absl_flags_private_handle_accessor.pc
%{_pkgconfigdir}/absl_flags_program_name.pc
%{_pkgconfigdir}/absl_flags_reflection.pc
%{_pkgconfigdir}/absl_flags_usage.pc
%{_pkgconfigdir}/absl_flags_usage_internal.pc
%{_pkgconfigdir}/absl_flat_hash_map.pc
%{_pkgconfigdir}/absl_flat_hash_set.pc
%{_pkgconfigdir}/absl_function_ref.pc
%{_pkgconfigdir}/absl_graphcycles_internal.pc
%{_pkgconfigdir}/absl_has_ostream_operator.pc
%{_pkgconfigdir}/absl_hash.pc
%{_pkgconfigdir}/absl_hash_container_defaults.pc
%{_pkgconfigdir}/absl_hash_function_defaults.pc
%{_pkgconfigdir}/absl_hash_policy_traits.pc
%{_pkgconfigdir}/absl_hashtable_control_bytes.pc
%{_pkgconfigdir}/absl_hashtable_debug.pc
%{_pkgconfigdir}/absl_hashtable_debug_hooks.pc
%{_pkgconfigdir}/absl_hashtable_profiler.pc
%{_pkgconfigdir}/absl_hashtablez_sampler.pc
%{_pkgconfigdir}/absl_inlined_vector.pc
%{_pkgconfigdir}/absl_inlined_vector_internal.pc
%{_pkgconfigdir}/absl_int128.pc
%{_pkgconfigdir}/absl_iterator_traits_internal.pc
%{_pkgconfigdir}/absl_iterator_traits_test_helper_internal.pc
%{_pkgconfigdir}/absl_kernel_timeout_internal.pc
%{_pkgconfigdir}/absl_layout.pc
%{_pkgconfigdir}/absl_leak_check.pc
%{_pkgconfigdir}/absl_log.pc
%{_pkgconfigdir}/absl_log_entry.pc
%{_pkgconfigdir}/absl_log_flags.pc
%{_pkgconfigdir}/absl_log_globals.pc
%{_pkgconfigdir}/absl_log_initialize.pc
%{_pkgconfigdir}/absl_log_internal_append_truncated.pc
%{_pkgconfigdir}/absl_log_internal_check_impl.pc
%{_pkgconfigdir}/absl_log_internal_check_op.pc
%{_pkgconfigdir}/absl_log_internal_conditions.pc
%{_pkgconfigdir}/absl_log_internal_config.pc
%{_pkgconfigdir}/absl_log_internal_flags.pc
%{_pkgconfigdir}/absl_log_internal_fnmatch.pc
%{_pkgconfigdir}/absl_log_internal_format.pc
%{_pkgconfigdir}/absl_log_internal_globals.pc
%{_pkgconfigdir}/absl_log_internal_log_impl.pc
%{_pkgconfigdir}/absl_log_internal_log_sink_set.pc
%{_pkgconfigdir}/absl_log_internal_message.pc
%{_pkgconfigdir}/absl_log_internal_nullguard.pc
%{_pkgconfigdir}/absl_log_internal_nullstream.pc
%{_pkgconfigdir}/absl_log_internal_proto.pc
%{_pkgconfigdir}/absl_log_internal_strip.pc
%{_pkgconfigdir}/absl_log_internal_structured.pc
%{_pkgconfigdir}/absl_log_internal_structured_proto.pc
%{_pkgconfigdir}/absl_log_internal_voidify.pc
%{_pkgconfigdir}/absl_log_severity.pc
%{_pkgconfigdir}/absl_log_sink.pc
%{_pkgconfigdir}/absl_log_sink_registry.pc
%{_pkgconfigdir}/absl_log_streamer.pc
%{_pkgconfigdir}/absl_log_structured.pc
%{_pkgconfigdir}/absl_malloc_internal.pc
%{_pkgconfigdir}/absl_memory.pc
%{_pkgconfigdir}/absl_meta.pc
%{_pkgconfigdir}/absl_no_destructor.pc
%{_pkgconfigdir}/absl_node_hash_map.pc
%{_pkgconfigdir}/absl_node_hash_set.pc
%{_pkgconfigdir}/absl_node_slot_policy.pc
%{_pkgconfigdir}/absl_non_temporal_arm_intrinsics.pc
%{_pkgconfigdir}/absl_non_temporal_memcpy.pc
%{_pkgconfigdir}/absl_nullability.pc
%{_pkgconfigdir}/absl_numeric.pc
%{_pkgconfigdir}/absl_numeric_representation.pc
%{_pkgconfigdir}/absl_optional.pc
%{_pkgconfigdir}/absl_overload.pc
%{_pkgconfigdir}/absl_periodic_sampler.pc
%{_pkgconfigdir}/absl_poison.pc
%{_pkgconfigdir}/absl_prefetch.pc
%{_pkgconfigdir}/absl_pretty_function.pc
%{_pkgconfigdir}/absl_profile_builder.pc
%{_pkgconfigdir}/absl_random_bit_gen_ref.pc
%{_pkgconfigdir}/absl_random_distributions.pc
%{_pkgconfigdir}/absl_random_internal_distribution_caller.pc
%{_pkgconfigdir}/absl_random_internal_distribution_test_util.pc
%{_pkgconfigdir}/absl_random_internal_entropy_pool.pc
%{_pkgconfigdir}/absl_random_internal_fast_uniform_bits.pc
%{_pkgconfigdir}/absl_random_internal_fastmath.pc
%{_pkgconfigdir}/absl_random_internal_generate_real.pc
%{_pkgconfigdir}/absl_random_internal_iostream_state_saver.pc
%{_pkgconfigdir}/absl_random_internal_mock_helpers.pc
%{_pkgconfigdir}/absl_random_internal_nonsecure_base.pc
%{_pkgconfigdir}/absl_random_internal_pcg_engine.pc
%{_pkgconfigdir}/absl_random_internal_platform.pc
%{_pkgconfigdir}/absl_random_internal_randen.pc
%{_pkgconfigdir}/absl_random_internal_randen_engine.pc
%{_pkgconfigdir}/absl_random_internal_randen_hwaes.pc
%{_pkgconfigdir}/absl_random_internal_randen_hwaes_impl.pc
%{_pkgconfigdir}/absl_random_internal_randen_slow.pc
%{_pkgconfigdir}/absl_random_internal_salted_seed_seq.pc
%{_pkgconfigdir}/absl_random_internal_seed_material.pc
%{_pkgconfigdir}/absl_random_internal_traits.pc
%{_pkgconfigdir}/absl_random_internal_uniform_helper.pc
%{_pkgconfigdir}/absl_random_internal_wide_multiply.pc
%{_pkgconfigdir}/absl_random_random.pc
%{_pkgconfigdir}/absl_random_seed_gen_exception.pc
%{_pkgconfigdir}/absl_random_seed_sequences.pc
%{_pkgconfigdir}/absl_raw_hash_map.pc
%{_pkgconfigdir}/absl_raw_hash_set.pc
%{_pkgconfigdir}/absl_raw_hash_set_resize_impl.pc
%{_pkgconfigdir}/absl_raw_logging_internal.pc
%{_pkgconfigdir}/absl_sample_recorder.pc
%{_pkgconfigdir}/absl_scoped_set_env.pc
%{_pkgconfigdir}/absl_span.pc
%{_pkgconfigdir}/absl_spinlock_wait.pc
%{_pkgconfigdir}/absl_stacktrace.pc
%{_pkgconfigdir}/absl_status.pc
%{_pkgconfigdir}/absl_statusor.pc
%{_pkgconfigdir}/absl_str_format.pc
%{_pkgconfigdir}/absl_str_format_internal.pc
%{_pkgconfigdir}/absl_strerror.pc
%{_pkgconfigdir}/absl_string_view.pc
%{_pkgconfigdir}/absl_strings.pc
%{_pkgconfigdir}/absl_strings_internal.pc
%{_pkgconfigdir}/absl_symbolize.pc
%{_pkgconfigdir}/absl_synchronization.pc
%{_pkgconfigdir}/absl_throw_delegate.pc
%{_pkgconfigdir}/absl_time.pc
%{_pkgconfigdir}/absl_time_zone.pc
%{_pkgconfigdir}/absl_tracing_internal.pc
%{_pkgconfigdir}/absl_type_traits.pc
%{_pkgconfigdir}/absl_utf8_for_code_point.pc
%{_pkgconfigdir}/absl_utility.pc
%{_pkgconfigdir}/absl_variant.pc
%{_pkgconfigdir}/absl_vlog_config_internal.pc
%{_pkgconfigdir}/absl_vlog_is_on.pc
%{_pkgconfigdir}/absl_weakly_mixed_integer.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libabsl_base.a
%{_libdir}/libabsl_city.a
%{_libdir}/libabsl_civil_time.a
%{_libdir}/libabsl_cord.a
%{_libdir}/libabsl_cord_internal.a
%{_libdir}/libabsl_cordz_functions.a
%{_libdir}/libabsl_cordz_handle.a
%{_libdir}/libabsl_cordz_info.a
%{_libdir}/libabsl_cordz_sample_token.a
%{_libdir}/libabsl_crc32c.a
%{_libdir}/libabsl_crc_cord_state.a
%{_libdir}/libabsl_crc_cpu_detect.a
%{_libdir}/libabsl_crc_internal.a
%{_libdir}/libabsl_debugging_internal.a
%{_libdir}/libabsl_decode_rust_punycode.a
%{_libdir}/libabsl_demangle_internal.a
%{_libdir}/libabsl_demangle_rust.a
%{_libdir}/libabsl_die_if_null.a
%{_libdir}/libabsl_examine_stack.a
%{_libdir}/libabsl_exponential_biased.a
%{_libdir}/libabsl_failure_signal_handler.a
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
%{_libdir}/libabsl_hashtable_profiler.a
%{_libdir}/libabsl_hashtablez_sampler.a
%{_libdir}/libabsl_int128.a
%{_libdir}/libabsl_kernel_timeout_internal.a
%{_libdir}/libabsl_leak_check.a
%{_libdir}/libabsl_log_entry.a
%{_libdir}/libabsl_log_flags.a
%{_libdir}/libabsl_log_globals.a
%{_libdir}/libabsl_log_initialize.a
%{_libdir}/libabsl_log_internal_check_op.a
%{_libdir}/libabsl_log_internal_conditions.a
%{_libdir}/libabsl_log_internal_fnmatch.a
%{_libdir}/libabsl_log_internal_format.a
%{_libdir}/libabsl_log_internal_globals.a
%{_libdir}/libabsl_log_internal_log_sink_set.a
%{_libdir}/libabsl_log_internal_message.a
%{_libdir}/libabsl_log_internal_nullguard.a
%{_libdir}/libabsl_log_internal_proto.a
%{_libdir}/libabsl_log_internal_structured_proto.a
%{_libdir}/libabsl_log_severity.a
%{_libdir}/libabsl_log_sink.a
%{_libdir}/libabsl_malloc_internal.a
%{_libdir}/libabsl_periodic_sampler.a
%{_libdir}/libabsl_poison.a
%{_libdir}/libabsl_profile_builder.a
%{_libdir}/libabsl_random_distributions.a
%{_libdir}/libabsl_random_internal_distribution_test_util.a
%{_libdir}/libabsl_random_internal_entropy_pool.a
%{_libdir}/libabsl_random_internal_platform.a
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
%{_libdir}/libabsl_strerror.a
%{_libdir}/libabsl_str_format_internal.a
%{_libdir}/libabsl_strings.a
%{_libdir}/libabsl_strings_internal.a
%{_libdir}/libabsl_string_view.a
%{_libdir}/libabsl_symbolize.a
%{_libdir}/libabsl_synchronization.a
%{_libdir}/libabsl_throw_delegate.a
%{_libdir}/libabsl_time.a
%{_libdir}/libabsl_time_zone.a
%{_libdir}/libabsl_tracing_internal.a
%{_libdir}/libabsl_utf8_for_code_point.a
%{_libdir}/libabsl_vlog_config_internal.a
%endif

%if %{with test_libs}
%files test
%defattr(644,root,root,755)
%{_libdir}/libabsl_atomic_hook_test_helper.so.%{abiver}
%{_libdir}/libabsl_exception_safety_testing.so.%{abiver}
%{_libdir}/libabsl_hash_generator_testing.so.%{abiver}
%{_libdir}/libabsl_log_internal_test_actions.so.%{abiver}
%{_libdir}/libabsl_log_internal_test_helpers.so.%{abiver}
%{_libdir}/libabsl_log_internal_test_matchers.so.%{abiver}
%{_libdir}/libabsl_per_thread_sem_test_common.so.%{abiver}
%{_libdir}/libabsl_pow10_helper.so.%{abiver}
%{_libdir}/libabsl_scoped_mock_log.so.%{abiver}
%{_libdir}/libabsl_spinlock_test_common.so.%{abiver}
%{_libdir}/libabsl_stack_consumption.so.%{abiver}
%{_libdir}/libabsl_status_matchers.so.%{abiver}
%{_libdir}/libabsl_test_instance_tracker.so.%{abiver}
%{_libdir}/libabsl_time_internal_test_util.so.%{abiver}

%files test-devel
%defattr(644,root,root,755)
%{_libdir}/libabsl_atomic_hook_test_helper.so
%{_libdir}/libabsl_exception_safety_testing.so
%{_libdir}/libabsl_hash_generator_testing.so
%{_libdir}/libabsl_log_internal_test_actions.so
%{_libdir}/libabsl_log_internal_test_helpers.so
%{_libdir}/libabsl_log_internal_test_matchers.so
%{_libdir}/libabsl_per_thread_sem_test_common.so
%{_libdir}/libabsl_pow10_helper.so
%{_libdir}/libabsl_scoped_mock_log.so
%{_libdir}/libabsl_spinlock_test_common.so
%{_libdir}/libabsl_stack_consumption.so
%{_libdir}/libabsl_status_matchers.so
%{_libdir}/libabsl_test_instance_tracker.so
%{_libdir}/libabsl_time_internal_test_util.so
%{_pkgconfigdir}/absl_atomic_hook_test_helper.pc
%{_pkgconfigdir}/absl_btree_test_common.pc
%{_pkgconfigdir}/absl_cord_rep_test_util.pc
%{_pkgconfigdir}/absl_cord_test_helpers.pc
%{_pkgconfigdir}/absl_cordz_test_helpers.pc
%{_pkgconfigdir}/absl_exception_safety_testing.pc
%{_pkgconfigdir}/absl_exception_testing.pc
%{_pkgconfigdir}/absl_hash_generator_testing.pc
%{_pkgconfigdir}/absl_hash_policy_testing.pc
%{_pkgconfigdir}/absl_hash_testing.pc
%{_pkgconfigdir}/absl_log_internal_test_actions.pc
%{_pkgconfigdir}/absl_log_internal_test_helpers.pc
%{_pkgconfigdir}/absl_log_internal_test_matchers.pc
%{_pkgconfigdir}/absl_per_thread_sem_test_common.pc
%{_pkgconfigdir}/absl_pow10_helper.pc
%{_pkgconfigdir}/absl_random_internal_explicit_seed_seq.pc
%{_pkgconfigdir}/absl_random_internal_mock_overload_set.pc
%{_pkgconfigdir}/absl_random_internal_mock_validators.pc
%{_pkgconfigdir}/absl_random_internal_sequence_urbg.pc
%{_pkgconfigdir}/absl_random_mocking_bit_gen.pc
%{_pkgconfigdir}/absl_scoped_mock_log.pc
%{_pkgconfigdir}/absl_spinlock_test_common.pc
%{_pkgconfigdir}/absl_spy_hash_state.pc
%{_pkgconfigdir}/absl_stack_consumption.pc
%{_pkgconfigdir}/absl_status_matchers.pc
%{_pkgconfigdir}/absl_test_allocator.pc
%{_pkgconfigdir}/absl_test_instance_tracker.pc
%{_pkgconfigdir}/absl_thread_pool.pc
%{_pkgconfigdir}/absl_time_internal_test_util.pc
%{_pkgconfigdir}/absl_tracked.pc
%{_pkgconfigdir}/absl_unordered_map_constructor_test.pc
%{_pkgconfigdir}/absl_unordered_map_lookup_test.pc
%{_pkgconfigdir}/absl_unordered_map_members_test.pc
%{_pkgconfigdir}/absl_unordered_map_modifiers_test.pc
%{_pkgconfigdir}/absl_unordered_set_constructor_test.pc
%{_pkgconfigdir}/absl_unordered_set_lookup_test.pc
%{_pkgconfigdir}/absl_unordered_set_members_test.pc
%{_pkgconfigdir}/absl_unordered_set_modifiers_test.pc

%if %{with static_libs}
%files test-static
%defattr(644,root,root,755)
%{_libdir}/libabsl_atomic_hook_test_helper.a
%{_libdir}/libabsl_exception_safety_testing.a
%{_libdir}/libabsl_hash_generator_testing.a
%{_libdir}/libabsl_log_internal_test_actions.a
%{_libdir}/libabsl_log_internal_test_helpers.a
%{_libdir}/libabsl_log_internal_test_matchers.a
%{_libdir}/libabsl_per_thread_sem_test_common.a
%{_libdir}/libabsl_pow10_helper.a
%{_libdir}/libabsl_scoped_mock_log.a
%{_libdir}/libabsl_spinlock_test_common.a
%{_libdir}/libabsl_stack_consumption.a
%{_libdir}/libabsl_status_matchers.a
%{_libdir}/libabsl_test_instance_tracker.a
%{_libdir}/libabsl_time_internal_test_util.a
%endif
%endif
