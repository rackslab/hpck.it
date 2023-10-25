%?python_enable_dependency_generator

# This package supports both old setuptools way of building packages with the
# setup.py script provided in RFL build package on RHEL8 and the modern way with
# wheels and pyproject.toml on other systems with more recent versions of
# Python, pip, setuptools and Python RPM macros.

Name:           rfl
Version:        {{ version }}
Release:        {{ release }}
Summary:        Rackslab Foundation Library

License:        GPLv3+
Group:          System Environment/Base
URL:            https://github.com/rackslab/RFL
{{ sources }}
{{ patches }}
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?rhel} && 0%{?rhel} <= 8
BuildRequires:  python3-tomli
%else
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif

Requires:       python3-%{name}-authorizations
Requires:       python3-%{name}-build
Requires:       python3-%{name}-core
Requires:       python3-%{name}-settings
Requires:       python3-%{name}-tokens
Requires:       python3-%{name}-web

%description
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package is a metapackage to install all RFL packages.

%package -n python3-%{name}-authorizations
Summary:        Rackslab Foundation Library: authorizations package
BuildArch:      noarch

%description -n python3-%{name}-authorizations
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes authorizations package of RFL.

%package -n python3-%{name}-build
Summary:        Rackslab Foundation Library: build package
BuildArch:      noarch

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

%package -n python3-%{name}-settings
Summary:        Rackslab Foundation Library: settings package
BuildArch:      noarch

%description -n python3-%{name}-settings
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes settings package of RFL.

%package -n python3-%{name}-tokens
Summary:        Rackslab Foundation Library: tokens package
BuildArch:      noarch

%description -n python3-%{name}-tokens
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes tokens package of RFL.

%package -n python3-%{name}-web
Summary:        Rackslab Foundation Library: web package
BuildArch:      noarch

%description -n python3-%{name}-web
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes web package of RFL.

%prep
{{ prep_sources }}
{{ prep_patches }}

%build
# Manually copy setup.py from build package into all packages top-folders so
# this script can be used by py3_build and py3_install macros on RHEL8.
%if 0%{?rhel} && 0%{?rhel} <= 8
cp src/build/rfl/build/scripts/setup.py src/core/
cp src/build/rfl/build/scripts/setup.py src/authorizations/
cp src/build/rfl/build/scripts/setup.py src/build/
cp src/build/rfl/build/scripts/setup.py src/settings/
cp src/build/rfl/build/scripts/setup.py src/tokens/
cp src/build/rfl/build/scripts/setup.py src/web/
%endif

# Note that this macro cannot be defined at the top of the spec file as global
# because buildsubdir which is part of py3_* and pyproject_* macros expansions
# is not yet defined at this stage. It is then defined locally and lately to
# ensure proper expansion.
%if 0%{?rhel} && 0%{?rhel} <= 8
%define _rfl_pybuild %{py3_build}
%else
%define _rfl_pybuild %{pyproject_wheel}
%endif

# start with core as other packages may depend on it.
cd %{_builddir}/%{buildsubdir}/src/core
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/authorizations
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/build
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/settings
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/tokens
%_rfl_pybuild
cd %{_builddir}/%{buildsubdir}/src/web
%_rfl_pybuild

%install

%if 0%{?rhel} && 0%{?rhel} <= 8
%define _rfl_pyinstall %{py3_install}
%else
%define _rfl_pyinstall %{pyproject_install}
%endif

cd %{_builddir}/%{buildsubdir}/src/core
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/authorizations
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/build
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/settings
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/tokens
%_rfl_pyinstall
cd %{_builddir}/%{buildsubdir}/src/web
%_rfl_pyinstall

%if 0%{?rhel} && 0%{?rhel} <= 8
%define _rfl_pysuffix egg-info
%else
%define _rfl_pysuffix dist-info
%endif

%files -n python3-%{name}-authorizations
%doc src/authorizations/README.md
%{python3_sitelib}/rfl/authorizations
%{python3_sitelib}/RFL.authorizations-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-build
%doc src/build/README.md
%{python3_sitelib}/rfl/build
%{python3_sitelib}/RFL.build-*.%{_rfl_pysuffix}/
%{_bindir}/install-setup-generator

%files -n python3-%{name}-core
%doc src/core/README.md
%{python3_sitelib}/rfl/core
%{python3_sitelib}/RFL.core-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-settings
%doc src/settings/README.md
%{python3_sitelib}/rfl/settings
%{python3_sitelib}/RFL.settings-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-tokens
%doc src/tokens/README.md
%{python3_sitelib}/rfl/tokens
%{python3_sitelib}/RFL.tokens-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-web
%doc src/web/README.md
%{python3_sitelib}/rfl/web
%{python3_sitelib}/RFL.web-*.%{_rfl_pysuffix}/

{{ changelog }}
