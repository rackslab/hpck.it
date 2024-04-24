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
%if 0%{?rhel}
BuildRequires:  python3-tomli
%endif

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

%if ! 0%{?rhel} || 0%{?rhel} >= 9
%generate_buildrequires
# Unfortunately, macros from pyproject-rpm-macros do not support sub-packages in
# packages namespace like RFL, then the macro is not able to detect the test
# dependencies. This is a reason why unit tests are not executed on package
# build.
%pyproject_buildrequires
%endif

%package -n python3-%{name}-authentication
Summary:        Rackslab Foundation Library: authentication package
BuildArch:      noarch

%description -n python3-%{name}-authentication
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes authentication package of RFL.

%package -n python3-%{name}-build
Summary:        Rackslab Foundation Library: build package
BuildArch:      noarch
Requires:       ninja-build

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

%description -n python3-%{name}-log
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes log package of RFL.

%package -n python3-%{name}-permissions
Summary:        Rackslab Foundation Library: permissions package
BuildArch:      noarch
# RFL tries to import cached_property from functools which is available starting
# from Python >= 3.8, and fallback to compatible cached_property external
# dependency otherwise. However, this optional dependency is not declared in
# pyproject.toml, because it is not required in most cases. Then it must be
# defined explicitely here when Python < 3.8.
Requires:       (python3dist(cached-property) if python3 < 3.8)

%description -n python3-%{name}-permissions
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes permissions package of RFL.

%package -n python3-%{name}-settings
Summary:        Rackslab Foundation Library: settings package
BuildArch:      noarch

%description -n python3-%{name}-settings
RFL is a Python library and a set of common utilities useful to most Rackslab
software solutions.

This package includes settings package of RFL.

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
# Manually copy setup script from build package into all packages top-folders so
# this script can be used by py3_build/py3_install macros on RHEL8 and
# pyproject_wheel/pyproject_install macros on RHEL9.
%if 0%{?rhel} && 0%{?rhel} <= 9
cp src/build/rfl/build/scripts/setup src/core/setup.py
cp src/build/rfl/build/scripts/setup src/authentication/setup.py
cp src/build/rfl/build/scripts/setup src/build/setup.py
cp src/build/rfl/build/scripts/setup src/log/setup.py
cp src/build/rfl/build/scripts/setup src/permissions/setup.py
cp src/build/rfl/build/scripts/setup src/settings/setup.py
cp src/build/rfl/build/scripts/setup src/web/setup.py
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

%if 0%{?rhel} && 0%{?rhel} <= 8
%define _rfl_pyinstall %{py3_install}
%else
%define _rfl_pyinstall %{pyproject_install}
%endif

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

%if 0%{?rhel} && 0%{?rhel} <= 8
%define _rfl_pysuffix egg-info
%else
%define _rfl_pysuffix dist-info
%endif

%files -n python3-%{name}-authentication
%doc src/authentication/README.md
%{python3_sitelib}/rfl/authentication
%{python3_sitelib}/RFL.authentication-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-build
%doc src/build/README.md
%{python3_sitelib}/rfl/build
%{python3_sitelib}/RFL.build-*.%{_rfl_pysuffix}/
%{_bindir}/rfl-install-setup-generator
%{_bindir}/rfl-project-version

%files -n python3-%{name}-core
%doc src/core/README.md
%{python3_sitelib}/rfl/core
%{python3_sitelib}/RFL.core-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-log
%doc src/log/README.md
%{python3_sitelib}/rfl/log
%{python3_sitelib}/RFL.log-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-permissions
%doc src/permissions/README.md
%{python3_sitelib}/rfl/permissions
%{python3_sitelib}/RFL.permissions-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-settings
%doc src/settings/README.md
%{python3_sitelib}/rfl/settings
%{python3_sitelib}/RFL.settings-*.%{_rfl_pysuffix}/

%files -n python3-%{name}-web
%doc src/web/README.md
%{python3_sitelib}/rfl/web
%{python3_sitelib}/RFL.web-*.%{_rfl_pysuffix}/

{{ changelog }}
