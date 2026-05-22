%{?python_enable_dependency_generator}

# This package supports both old setuptools way of building packages with the
# setup.py script provided in RFL build package on RHEL8 and the modern way with
# wheels and pyproject.toml on other systems with more recent versions of
# Python, pip, setuptools and Python RPM macros.

Name:           rfl
Version:        {{ version }}
Release:        {{ release }}
Summary:        Rackslab Foundation Library

License:        LGPL-3.0-or-later
Group:          System Environment/Base
URL:            https://github.com/rackslab/RFL
{{ sources }}
{{ patches }}
BuildArch:      noarch
BuildRequires:  python3-devel
{% if pkg.distribution in ["suse15", "suse16"] %}
BuildRequires:  python-rpm-macros
BuildRequires:  python-rpm-generators
BuildRequires:  fdupes
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
{% endif %}
{% if pkg.distribution in ["el8", "el9", "suse15", "suse16"] %}
BuildRequires:  python3-tomli
{% endif %}

Requires:       python3-%{name}-authentication
Requires:       python3-%{name}-build
Requires:       python3-%{name}-core
Requires:       python3-%{name}-log
Requires:       python3-%{name}-permissions
Requires:       python3-%{name}-settings
Requires:       python3-%{name}-web

%description
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package is a metapackage to install all RFL packages.

{# pyproject_buildrequires macro is not supported on el8 and suse #}
{% if pkg.distribution not in ["el8", "suse15", "suse16"] %}
%generate_buildrequires
{% if pkg.distribution in ["el9"] %}
# Manually copy setup script from build package for pyproject_buildrequires
# macro on RHEL9 because pyproject.toml is not supported on this version.
cp src/build/rfl/build/scripts/setup setup.py
{% endif %}
# Install build and tests requirements declared in main pyproject.toml (actual
# runtime dependencies are declared in namespace packages in RFL).
%pyproject_buildrequires -x tests
{% endif %}

# python3-rfl-authentication — transitional packaging (step 1 of 3)
#
# Step 1 (current): this subpackage still hard-Requires -jwt and -ldap so existing
# dependents (e.g. slurm-web) that only require python3-rfl-authentication keep
# JWT/LDAP support on upgrade. Extra subpackages must not Require this package
# while it pulls them in (same constraint as Debian: avoid a Requires cycle).
#
# Step 2: every in-repo and published dependent that needs JWT/LDAP/OIDC must
# require the all-extras subpackage or a specific extra (on el9+/Fedora:
# python3-rfl-authentication+all or +EXTRA; on el8/openSUSE: -all, -jwt, -ldap, -oidc).
#
# Step 3 (light base): remove the two Requires lines on -jwt and -ldap below; keep
# only python3-rfl-core (and distribution-specific Requires above). Each
# python3-rfl-authentication-* extra must Require python3-rfl-authentication
# (= {version}-{release}) instead of python3-rfl-core alone (this subpackage
# owns the rfl.authentication module). Optional: Suggests: python3-rfl-authentication+all
# (or -all on el8/openSUSE) on this subpackage for softer upgrades. Do not apply step 3
# until step 2 is complete.

{# auth_legacy_extras: el8 and openSUSE lack %pyproject_extras_subpkg (+EXTRA naming).
   Use hyphenated RPM subpackages (-jwt, -ldap, -oidc on suse16, -all) with explicit
   Requires instead of python3-rfl-authentication+EXTRA / +all from dist-info. #}
{% set auth_legacy_extras = pkg.distribution in ["el8", "suse15", "suse16"] %}
{# auth_suse_extras: within the legacy branch, openSUSE uses python3-* RPM names for
   optional libraries; el8 uses python3dist(...) (RHEL-style generator names). #}
{% set auth_suse_extras = pkg.distribution in ["suse15", "suse16"] %}

%package -n python3-%{name}-authentication
Summary:        Rackslab Foundation Library: authentication package
BuildArch:      noarch
# Python dependency generator does not set core requirement on every distribution.
Requires:       python3-%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
{% if auth_legacy_extras %}
# Transitional (step 1): hyphenated extra subpackages (el8/openSUSE: no +EXTRA macro).
Requires:       python3-%{name}-authentication-jwt = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-%{name}-authentication-ldap = %{?epoch:%{epoch}:}%{version}-%{release}
{% else %}
# Transitional (step 1): extras subpackages are python3-rfl-authentication+EXTRA.
Requires:       python3-%{name}-authentication+jwt = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-%{name}-authentication+ldap = %{?epoch:%{epoch}:}%{version}-%{release}
{% endif %}

%description -n python3-%{name}-authentication
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes authentication package of RFL.

This is a transitional package: it installs the base authentication module and
pulls jwt and ldap optional dependencies for backward compatibility. New
packages must depend on python3-rfl-authentication+all (or -all on el8/openSUSE)
or specific extra subpackages instead.

{# %pyproject_extras_subpkg is not supported on el8 and openSUSE. #}
{% if auth_legacy_extras %}
%package -n python3-%{name}-authentication-jwt
Summary:        Rackslab Foundation Library: authentication JWT extra
BuildArch:      noarch
Requires:       python3-%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
{% if auth_suse_extras %}
Requires:       python3-PyJWT
{% else %}
Requires:       python3dist(pyjwt)
{% endif %}
{% if pkg.distribution == "el8" %}
Provides:       python3dist(rfl-authentication[jwt]) = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       python%{python3_version}dist(rfl-authentication[jwt]) = %{?epoch:%{epoch}:}%{version}-%{release}
{% endif %}

%description -n python3-%{name}-authentication-jwt
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package provides JWT optional dependencies for RFL authentication.

%package -n python3-%{name}-authentication-ldap
Summary:        Rackslab Foundation Library: authentication LDAP extra
BuildArch:      noarch
Requires:       python3-%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
{% if auth_suse_extras %}
Requires:       python3-ldap
{% else %}
Requires:       python3dist(python-ldap)
{% endif %}
{% if pkg.distribution == "el8" %}
Provides:       python3dist(rfl-authentication[ldap]) = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       python%{python3_version}dist(rfl-authentication[ldap]) = %{?epoch:%{epoch}:}%{version}-%{release}
{% endif %}

%description -n python3-%{name}-authentication-ldap
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package provides LDAP optional dependencies for RFL authentication.

{% if pkg.distribution == "suse16" %}
%package -n python3-%{name}-authentication-oidc
Summary:        Rackslab Foundation Library: authentication OIDC extra
BuildArch:      noarch
Requires:       python3-%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-Authlib
Requires:       python3-Flask
Requires:       python3-requests

%description -n python3-%{name}-authentication-oidc
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package provides OIDC optional dependencies for RFL authentication.
{% endif %}

%package -n python3-%{name}-authentication-all
Summary:        Rackslab Foundation Library: authentication all extras
BuildArch:      noarch
Requires:       python3-%{name}-authentication = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-%{name}-authentication-jwt = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-%{name}-authentication-ldap = %{?epoch:%{epoch}:}%{version}-%{release}
{% if pkg.distribution == "suse16" %}
Requires:       python3-%{name}-authentication-oidc = %{?epoch:%{epoch}:}%{version}-%{release}
{% endif %}
{% if pkg.distribution == "el8" %}
Provides:       python3dist(rfl-authentication[all]) = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       python%{python3_version}dist(rfl-authentication[all]) = %{?epoch:%{epoch}:}%{version}-%{release}
{% endif %}

%description -n python3-%{name}-authentication-all
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This metapackage installs all RFL authentication optional dependencies. New
packages requiring full authentication support must depend on this package.
{% else %}
{# -i glob must match installed dist-info (Fedora: PEP 503 rfl_authentication-*; RHEL: RFL.authentication-*). #}
{% if pkg.distribution.startswith("fc") %}
%pyproject_extras_subpkg -n python3-%{name}-authentication -i %{python3_sitelib}/rfl_authentication-*.dist-info jwt ldap oidc all
{% else %}
%pyproject_extras_subpkg -n python3-%{name}-authentication -i %{python3_sitelib}/RFL.authentication-*.dist-info jwt ldap oidc all
{% endif %}
{% endif %}

%package -n python3-%{name}-build
Summary:        Rackslab Foundation Library: build package
BuildArch:      noarch
{% if pkg.distribution == "suse15" %}
# Automatic dependency generator does not work on suse15, dependencies must
# be explicitely declared for this distribution.
Requires:       python3-%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-tomli
{% endif %}
{% if pkg.distribution in ["suse15", "suse16"] %}
Requires:       ninja
{% else %}
Requires:       ninja-build
{% endif %}

%description -n python3-%{name}-build
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes build package of RFL.

%package -n python3-%{name}-core
Summary:        Rackslab Foundation Library: core package
BuildArch:      noarch

%description -n python3-%{name}-core
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes core package of RFL.

%package -n python3-%{name}-log
Summary:        Rackslab Foundation Library: log package
BuildArch:      noarch
{% if pkg.distribution == "suse15" %}
# Automatic dependency generator does not work on suse15, dependencies must
# be explicitely declared for this distribution.
Requires:       python3-%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
{% endif %}

%description -n python3-%{name}-log
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes log package of RFL.

%package -n python3-%{name}-permissions
Summary:        Rackslab Foundation Library: permissions package
BuildArch:      noarch
{% if pkg.distribution == "suse15" %}
# Automatic dependency generator does not work on suse15, dependencies must
# be explicitely declared for this distribution.
Requires:       python3-%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-%{name}-authentication = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-PyYAML
{% endif %}
{% if pkg.distribution == "suse15" %}
# RFL tries to import cached_property from functools which is available
# starting from Python >= 3.8, and fallback to compatible cached_property
# external dependency otherwise. This optional dependency is not declared in
# pyproject.toml, because it is not required in most cases. Then it
# must be defined explicitely here for suse15 with Python 3.6.
Requires:       python3-cached-property
{% elif pkg.distribution == "el8" %}
# RFL tries to import cached_property from functools which is available
# starting from Python >= 3.8, and fallback to compatible cached_property
# external dependency otherwise. This optional dependency is not declared in
# pyproject.toml, because it is not required in most cases. Then it
# must be defined explicitely here for el8 with Python 3.6.
Requires:       python3dist(cached-property)
{% endif %}

%description -n python3-%{name}-permissions
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes permissions package of RFL.

%package -n python3-%{name}-settings
Summary:        Rackslab Foundation Library: settings package
BuildArch:      noarch
{% if pkg.distribution == "suse15" %}
# Automatic dependency generator does not work on suse15, dependencies must be
# explicitely declared for this distribution.
Requires:       python3-%{name}-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-PyYAML
{% endif %}

%description -n python3-%{name}-settings
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes settings package of RFL.

%package -n python3-%{name}-web
Summary:        Rackslab Foundation Library: web package
BuildArch:      noarch
{% if auth_legacy_extras %}
# el8/openSUSE: hyphenated extra subpackages; declare JWT extra explicitly.
Requires:       python3-%{name}-authentication-jwt = %{?epoch:%{epoch}:}%{version}-%{release}
{% if pkg.distribution == "suse15" %}
Requires:       python3-%{name}-permissions = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-Flask
{% endif %}
{% endif %}

%description -n python3-%{name}-web
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes web package of RFL.

%prep
{{ prep_sources }}
{{ prep_patches }}

%build
# Manually copy setup script from build package into all packages top-folders so
# this script can be used by py3_build/py3_install macros on RHEL8 and
# pyproject_wheel/pyproject_install macros on RHEL9.
{% if pkg.distribution in ["el8", "el9", "suse15", "suse16"] %}
cp src/build/rfl/build/scripts/setup src/core/setup.py
cp src/build/rfl/build/scripts/setup src/authentication/setup.py
cp src/build/rfl/build/scripts/setup src/build/setup.py
cp src/build/rfl/build/scripts/setup src/log/setup.py
cp src/build/rfl/build/scripts/setup src/permissions/setup.py
cp src/build/rfl/build/scripts/setup src/settings/setup.py
cp src/build/rfl/build/scripts/setup src/web/setup.py
{% endif %}

# Note that this macro cannot be defined at the top of the spec file as global
# because buildsubdir which is part of py3_* and pyproject_* macros expansions
# is not yet defined at this stage. It is then defined locally and lately to
# ensure proper expansion.
{% if pkg.distribution == "el8" %}
%define _rfl_pybuild %{py3_build}
{% else %}
%define _rfl_pybuild %{pyproject_wheel}
{% endif %}

# start with core as other packages may depend on it.
cd %{_builddir}/%{buildsubdir}/src/core
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/authentication
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/build
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/log
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/permissions
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/settings
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/web
%_rfl_pybuild

%install

{% if pkg.distribution == "el8" %}
%define _rfl_pyinstall %{py3_install}
{% else %}
%define _rfl_pyinstall %{pyproject_install}
{% endif %}

cd %{_builddir}/%{buildsubdir}/src/core
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/authentication
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/build
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/log
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/permissions
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/settings
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/web
%_rfl_pyinstall

{% if pkg.distribution in ["suse15", "suse16"] %}
%python_expand %fdupes %{buildroot}%{$python_sitelib}
{% endif %}

{% if pkg.distribution == "el8" %}
%define _rfl_pysuffix egg-info
{% else %}
%define _rfl_pysuffix dist-info
{% endif %}

{# Macro pyproject_buildrequires is not supported on el8 and suse, so there #}
{# is no way to install tests requirements, hence run unit tests, on these  #}
{# distributions. #}
{% if pkg.distribution not in ["el8", "suse15", "suse16"] %}
%check
# Run pytest to execute unit tests, except on RHEL8 because testing dependencies
# are not automatically installed by generate_buildrequires macro on this
# distribution.
%pytest --import-mode=importlib
{% endif %}

%files -n python3-%{name}-authentication
%doc src/authentication/README.md
%{python3_sitelib}/rfl/authentication
%{python3_sitelib}/*authentication-*.%{_rfl_pysuffix}/

{% if auth_legacy_extras %}
%files -n python3-%{name}-authentication-jwt
%files -n python3-%{name}-authentication-ldap
{% if pkg.distribution == "suse16" %}
%files -n python3-%{name}-authentication-oidc
{% endif %}
%files -n python3-%{name}-authentication-all
{% endif %}

%files -n python3-%{name}-build
%doc src/build/README.md
%{python3_sitelib}/rfl/build
%{python3_sitelib}/*build-*.%{_rfl_pysuffix}/
%{_bindir}/rfl-install-setup-generator
%{_bindir}/rfl-project-version

%files -n python3-%{name}-core
%doc src/core/README.md
%{python3_sitelib}/rfl/core
%{python3_sitelib}/*core-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-log
%doc src/log/README.md
%{python3_sitelib}/rfl/log
%{python3_sitelib}/*log-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-permissions
%doc src/permissions/README.md
%{python3_sitelib}/rfl/permissions
%{python3_sitelib}/*permissions-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-settings
%doc src/settings/README.md
%{python3_sitelib}/rfl/settings
%{python3_sitelib}/*settings-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-web
%doc src/web/README.md
%{python3_sitelib}/rfl/web
%{python3_sitelib}/*web-*.%{_rfl_pysuffix}/

{{ changelog }}
