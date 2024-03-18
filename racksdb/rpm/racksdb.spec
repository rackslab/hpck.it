%?python_enable_dependency_generator

# This package supports both old setuptools way of building packages with the
# setup.py script provided in RFL build package on RHEL8 and the modern way with
# wheels and pyproject.toml on other systems with more recent versions of
# Python, pip, setuptools and Python RPM macros.

Name:           racksdb
Version:        {{ version }}
Release:        {{ release }}

License:        GPLv3+
Group:          System Environment/Base
URL:            https://github.com/rackslab/RacksDB
{{ sources }}
{{ patches }}
BuildRequires:  python3-devel
%if 0%{?rhel}
BuildRequires:  python3-rfl-build
%endif
BuildRequires:  make
BuildRequires:  asciidoctor
BuildRequires:  pango

Summary:        YAML database of datacenter infrastructures: CLI
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
RacksDB is an open source solution to modelize your datacenters infrastructures
in a simple YAML-based database to store information about the equipments in
your datacenters.

This package contains the CLI tool to request the database and draw diagrams of
its content.

%pyproject_extras_subpkg -n python3-%{name} web

%if ! 0%{?rhel} || 0%{?rhel} >= 9
%generate_buildrequires
%if 0%{?rhel}
rfl-install-setup-generator > /dev/null
%endif
# Include optional dependencies from web extra as they are required to run
# checks.
%pyproject_buildrequires -x web
%endif

%package -n python3-%{name}
Summary:        YAML database of datacenter infrastructures: Python Library
BuildArch:      noarch
Requires:       pango

%description -n python3-%{name}
RacksDB is an open source solution to modelize your datacenters infrastructures
in a simple YAML-based database to store information about the equipments in
your datacenters.

This package contains the Python library to load the database and explore its
content.

{% if pkg.distribution == "el8" %}
# Similar package is automatically generated thanks to pyproject_extras_subpkg
# macro in other distributions. It must be defined with explicit dependencies
# on el8 because this macro is not supported on this distribution.
%package -n python3-%{name}-web
Summary:        YAML database of datacenter infrastructures: Python Library for web app
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3dist(flask)
Requires:       python3dist(requests-toolbelt)
Provides:       python3dist(racksdb[web]) = %{?epoch:%{epoch}:}%{version}-%{release}

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
{% if pkg.distribution == "el8" %}
# On systems that are not RHEL8, extra subpackages are automatically built with
# web specific optional dependencies. This package must depend on this
# subpackage to indirectly depend on these requirements.
Requires:       python3-%{name}+web = %{?epoch:%{epoch}:}%{version}-%{release}
{% else %}
Requires:       python3-%{name}-web = %{?epoch:%{epoch}:}%{version}-%{release}
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
%if 0%{?rhel}
rfl-install-setup-generator
%endif
%if 0%{?rhel} && 0%{?rhel} <= 8
%py3_build
%else
%pyproject_wheel
%endif
make -C docs man

%install
%if 0%{?rhel} && 0%{?rhel} <= 8
%py3_install
%else
%pyproject_install
%pyproject_save_files racksdb
%endif

# empty configuration directory
install -d %{buildroot}%{_sysconfdir}/racksdb

# schemas
install -d %{buildroot}%{_datadir}/racksdb/schemas
install -p -m 0644 schemas/*.yml %{buildroot}%{_datadir}/racksdb/schemas

# empty database directory
install -d %{buildroot}%{_sharedstatedir}/racksdb

# man pages
install -d %{buildroot}%{_mandir}/man1
install -p -m 0644 docs/man/*.1 %{buildroot}%{_mandir}/man1/

%if 0%{?rhel} && 0%{?rhel} <= 8
%define _racksdb_pysuffix egg-info
%else
%define _racksdb_pysuffix dist-info
%endif

# Except on RHEL8 where it is not supported, run pyproject_check_import on all
# packages modules.
%if !0%{?rhel} || 0%{?rhel} >= 9
%check
%pyproject_check_import
%{python3} -m unittest
%endif

%files
%{_bindir}/racksdb
%doc %{_mandir}/man1/racksdb.*

%files -n python3-%{name}
%license LICENSE
%doc README.md
%doc examples
%{python3_sitelib}/racksdb/
%{python3_sitelib}/RacksDB-*.%{_racksdb_pysuffix}/
%{_sysconfdir}/racksdb
%{_datadir}/racksdb
%{_sharedstatedir}/racksdb

{% if pkg.distribution == "el8" %}
%files -n python3-%{name}-web
{% endif %}

%files -n %{name}-web
%{_bindir}/racksdb-web
%doc %{_mandir}/man1/racksdb-web.*

{{ changelog }}
