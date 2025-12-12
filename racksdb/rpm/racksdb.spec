%{?python_enable_dependency_generator}

# This package supports both old setuptools way of building packages with the
# setup.py script provided in RFL build package on RHEL8 and the modern way with
# wheels and pyproject.toml on other systems with more recent versions of
# Python, pip, setuptools and Python RPM macros.

Name:           racksdb
Version:        {{ version }}
Release:        {{ release }}

License:        MIT
Group:          System Environment/Base
URL:            https://github.com/rackslab/RacksDB
{{ sources }}
{{ patches }}
BuildRequires:  python3-devel
BuildRequires:  python3-rfl-build
{% if pkg.distribution == "el8" %}
# PyYAML library is required for docs/update-materials script. It does not have
# to be explicitely declared as build requirement except on el8 because it is
# also a build requirement of RacksDB itself and is automatically detected and
# declared by pyproject_buildrequires macro on other distributions.
BuildRequires:  python3-pyyaml
{% endif %}
{% if pkg.distribution in ["suse15", "suse16"] %}
BuildRequires:  python-rpm-macros
BuildRequires:  python-rpm-generators
BuildRequires:  fdupes
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
# PyYAML library is required for docs/update-materials script. It does not have
# to be explicitely declared as build requirement except on suse because it is
# also a build requirement of RacksDB itself and is automatically detected and
# declared by pyproject_buildrequires macro on other distributions
BuildRequires:  python3-PyYAML
# pyproject_buildrequires macro is not supported on openSUSE, build and tests
# dependencies must be explicitely declared for these distributions.
BuildRequires:  pango-devel
BuildRequires:  python3-cairo
BuildRequires:  python3-clustershell
BuildRequires:  python3-Flask
BuildRequires:  python3-gobject-cairo
BuildRequires:  python3-parameterized
BuildRequires:  python3-pytest
BuildRequires:  python3-requests-toolbelt
BuildRequires:  python3-rfl-log
{% endif %}
{% if pkg.distribution == "el8" %}
# On RHEL8, versions constraints must be set to ensure nodejs and npm are
# selected from nodejs:18 DNF module.
BuildRequires:  nodejs(engine) >= 18
BuildRequires:  npm(npm) >= 10
{% else %}
BuildRequires:  nodejs(engine)
BuildRequires:  npm
{% endif %}

BuildRequires:  make
{% if pkg.distribution == "suse15" %}
BuildRequires:  ruby2.5-rubygem-asciidoctor
{% elif pkg.distribution == "suse16" %}
BuildRequires:  ruby3.4-rubygem-asciidoctor
{% else %}
BuildRequires:  asciidoctor
{% endif %}
BuildRequires:  pango
BuildRequires:  python3-gobject
Summary:        YAML database of datacenter infrastructures: CLI
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
RacksDB is an open source solution to modelize your datacenters infrastructures
in a simple YAML-based database to store information about the equipments in
your datacenters.

This package contains the CLI tool to request the database and draw diagrams of
its content.

{# This macro is not supported on openSUSE #}
{% if pkg.distribution not in ["suse15", "suse16"] %}
%pyproject_extras_subpkg -n python3-%{name} web
{% endif %}

{# %pyproject_buildrequires macro is not supported on el8 and suse #}
{% if pkg.distribution not in ["el8", "suse15", "suse16"] %}
%generate_buildrequires
%if 0%{?rhel}
rfl-install-setup-generator > /dev/null
%endif
# Include optional dependencies from web extra as they are required to run
# checks.
%pyproject_buildrequires -x web -x tests
{% endif %}

%package -n python3-%{name}
Summary:        YAML database of datacenter infrastructures: Python Library
BuildArch:      noarch
Requires:       pango
{% if pkg.distribution in ["suse15", "suse16"] %}
Requires:       typelib(Pango)
{% endif %}
# RPM python dependency generator automatically translate PyGObject Python
# package to python3dist(pygobject) requirement. This requirement is satisfied
# by python3-gobject-base RPM package but unfortunately, this package does not
# include Cairo related stuff. This is fixed with this explicit dependency
# declaration.
Requires:       python3-gobject
{% if pkg.distribution == "suse15" %}
# Automatic dependency generator does not work on suse15, dependencies must
# be explicitely declared for this distribution.
Requires:       python3-cairo
Requires:       python3-clustershell
Requires:       python3-gobject-cairo
Requires:       python3-PyYAML
Requires:       python3-rfl-log
# RacksDB tries to import cached_property from functools which is available
# starting from Python >= 3.8, and fallback to compatible cached_property
# external dependency otherwise. This optional dependency is not declared in
# pyproject.toml, because it is not required in most cases. Then it
# must be defined explicitely here for suse15 with Python 3.6. The same
# rationale applies to importlib-metadata as well.
Requires:       python3-cached-property
Requires:       python3-importlib-metadata
{% elif pkg.distribution == "el8" %}
# RacksDB tries to import cached_property from functools which is available
# starting from Python >= 3.8, and fallback to compatible cached_property
# external dependency otherwise. This optional dependency is not declared in
# pyproject.toml, because it is not required in most cases. Then it
# must be defined explicitely here for el8 with Python 3.6. The same rationale
# applies to importlib-metadata as well.
Requires:       python3dist(cached-property)
Requires:       python3dist(importlib-metadata)
{% endif %}

%description -n python3-%{name}
RacksDB is an open source solution to modelize your datacenters infrastructures
in a simple YAML-based database to store information about the equipments in
your datacenters.

This package contains the Python library to load the database and explore its
content.

{% if pkg.distribution in ["el8", "suse15", "suse16"] %}
# Similar package is automatically generated thanks to pyproject_extras_subpkg
# macro in other distributions. It must be defined with explicit dependencies
# on el8 and openSUSE because this macro is not supported on this distribution.
%package -n python3-%{name}-web
Summary:        YAML database of datacenter infrastructures: Python Library for web app
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
{% if pkg.distribution == "el8" %}
Requires:       python3dist(flask)
Requires:       python3dist(requests-toolbelt)
Provides:       python3dist(racksdb[web]) = %{?epoch:%{epoch}:}%{version}-%{release}
{% elif pkg.distribution in ["suse15", "suse16"] %}
Requires:       python3-Flask
Requires:       python3-requests-toolbelt
{% endif %}

%description -n python3-%{name}-web
RacksDB is an open source solution to modelize your datacenters infrastructures
in a simple YAML-based database to store information about the equipments in
your datacenters.

This package contains the Python library for the web application.
{% endif %}

%package -n %{name}-web
Summary:        YAML database of datacenter infrastructures: REST API
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
{% if pkg.distribution in ["el8", "suse15", "suse16"] %}
# On RHEL8 and openSUSE systems, an additional -web meta-package is generated
# with all web specific optional dependencies. This package must depend on this
# subpackage to indirectly depend on these requirements.
Requires:       python3-%{name}-web = %{?epoch:%{epoch}:}%{version}-%{release}
{% else %}
# On all systems except RHEL >= 9 and Fedora, extra +web subpackage is
# automatically built with web specific optional dependencies. This package must
# depend on this subpackage to indirectly depend on these requirements.
Requires:       python3-%{name}+web = %{?epoch:%{epoch}:}%{version}-%{release}
{% endif %}

%description -n %{name}-web
RacksDB is an open source solution to modelize your datacenters infrastructures
in a simple YAML-based database to store information about the equipments in
your datacenters.

This package contains the web application with a REST API to request the
database and draw diagrams of its content.

%prep
{{ prep_sources }}
{{ prep_patches }}

%build
{% if pkg.distribution in ["el8", "el9", "suse15"] %}
rfl-install-setup-generator
{% endif %}
{% if pkg.distribution == "el8" %}
%py3_build
{% else %}
%pyproject_wheel
{% endif %}

# Generate manpages
docs/update-materials man

# Move node_modules from supplemental archive in frontend/ folder and remove
# symlink created by fatbuildr prescript patch in top folder. This is required
# by leaflet that refuses to build with node_modules in top folder.
NODE_MODULES=$(readlink node_modules)
mv ${NODE_MODULES} frontend/node_modules
rm node_modules

# Build frontend app
npm --prefix=frontend run build

# Restore node_modules directory and symlink in their initial state.
mv frontend/node_modules ${NODE_MODULES}
ln -s ${NODE_MODULES} node_modules

%install
{% if pkg.distribution == "el8" %}
%py3_install
{% else %}
%pyproject_install
{% if pkg.distribution not in ["suse15", "suse16"] %}
%pyproject_save_files racksdb
{% endif %}
{% endif %}

{% if pkg.distribution in ["suse15", "suse16"] %}
%python_expand %fdupes %{buildroot}%{$python_sitelib}
{% endif %}

# empty configuration directory
install -d %{buildroot}%{_sysconfdir}/racksdb

# schemas
install -d %{buildroot}%{_datadir}/racksdb/schemas
install -p -m 0644 schemas/*.yml %{buildroot}%{_datadir}/racksdb/schemas

# empty database directory
install -d %{buildroot}%{_sharedstatedir}/racksdb

# Install frontend application in datadir
cp -vdr --no-preserve=ownership frontend/dist %{buildroot}%{_datadir}/racksdb/frontend

# man pages
install -d %{buildroot}%{_mandir}/man1
install -p -m 0644 docs/man/*.1 %{buildroot}%{_mandir}/man1/

{% if pkg.distribution == "el8" %}
%define _racksdb_pysuffix egg-info
{% else %}
%define _racksdb_pysuffix dist-info
{% endif %}

{% if pkg.distribution != "el8" %}
%check
{% if pkg.distribution not in ["suse15", "suse16"] %}
# Except on RHEL8 and openSUSE where it is not supported, run
# pyproject_check_import on all packages modules.
%pyproject_check_import
{% endif %}
# Run pytest to execute unit tests, except on RHEL8 because testing dependencies
# are not automatically installed by generate_buildrequires macro on this
# distribution.
%pytest
{% endif %}

%files
%{_bindir}/racksdb
%doc %{_mandir}/man1/racksdb.*

%files -n python3-%{name}
%license LICENSE
%doc README.md
%doc examples
%{python3_sitelib}/racksdb/
%{python3_sitelib}/*-*.%{_racksdb_pysuffix}/
%{_sysconfdir}/racksdb
%{_datadir}/racksdb/schemas
%{_sharedstatedir}/racksdb

{% if pkg.distribution in ["el8", "suse15", "suse16"] %}
%files -n python3-%{name}-web
{% endif %}

%files -n %{name}-web
%{_bindir}/racksdb-web
%doc %{_mandir}/man1/racksdb-web.*
%{_datadir}/racksdb/frontend

{{ changelog }}
