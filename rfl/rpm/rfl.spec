%?python_enable_dependency_generator

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
BuildRequires:  python3-tomli

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
cp src/build/rfl/build/scripts/setup.py src/core/
cp src/build/rfl/build/scripts/setup.py src/authorizations/
cp src/build/rfl/build/scripts/setup.py src/build/
cp src/build/rfl/build/scripts/setup.py src/settings/
cp src/build/rfl/build/scripts/setup.py src/tokens/
cp src/build/rfl/build/scripts/setup.py src/web/

# start with core as other packages may depend on it.
cd %{_builddir}/%{buildsubdir}/src/core
%py3_build
cd %{_builddir}/%{buildsubdir}/src/authorizations
%py3_build
cd %{_builddir}/%{buildsubdir}/src/build
%py3_build
cd %{_builddir}/%{buildsubdir}/src/settings
%py3_build
cd %{_builddir}/%{buildsubdir}/src/tokens
%py3_build
cd %{_builddir}/%{buildsubdir}/src/web
%py3_build

%install
cd %{_builddir}/%{buildsubdir}/src/core
%py3_install
cd %{_builddir}/%{buildsubdir}/src/authorizations
%py3_install
cd %{_builddir}/%{buildsubdir}/src/build
%py3_install
cd %{_builddir}/%{buildsubdir}/src/settings
%py3_install
cd %{_builddir}/%{buildsubdir}/src/tokens
%py3_install
cd %{_builddir}/%{buildsubdir}/src/web
%py3_install

%files -n python3-%{name}-authorizations
%doc src/authorizations/README.md
%{python3_sitelib}/rfl/authorizations
%{python3_sitelib}/RFL.authorizations-*.egg-info/

%files -n python3-%{name}-build
%doc src/build/README.md
%{python3_sitelib}/rfl/build
%{python3_sitelib}/RFL.build-*.egg-info/
%{_bindir}/install-setup-generator

%files -n python3-%{name}-core
%doc src/core/README.md
%{python3_sitelib}/rfl/core
%{python3_sitelib}/RFL.core-*.egg-info/

%files -n python3-%{name}-settings
%doc src/settings/README.md
%{python3_sitelib}/rfl/settings
%{python3_sitelib}/RFL.settings-*.egg-info/

%files -n python3-%{name}-tokens
%doc src/tokens/README.md
%{python3_sitelib}/rfl/tokens
%{python3_sitelib}/RFL.tokens-*.egg-info/

%files -n python3-%{name}-web
%doc src/web/README.md
%{python3_sitelib}/rfl/web
%{python3_sitelib}/RFL.web-*.egg-info/

{{ changelog }}
