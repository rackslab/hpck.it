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
BuildRequires:  python3-setuptools
%if 0%{?rhel} && 0%{?rhel} <= 8
BuildRequires:  python3-rfl-build
%else
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif
BuildRequires:  make
BuildRequires:  asciidoctor

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

%package -n python3-%{name}
Summary:        YAML database of datacenter infrastructures: Python Library
BuildArch:      noarch

%description -n python3-%{name}
RacksDB is an open source solution to modelize your datacenters infrastructures
in a simple YAML-based database to store information about the equipments in
your datacenters.

This package contains the Python library to load the database and explore its
content.

%package -n %{name}-web
Summary:        YAML database of datacenter infrastructures: REST API
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%if ! 0%{?rhel} || 0%{?rhel} > 8
# On systems that are not RHEL8, extra subpackages are automatically built with
# web specific optional dependencies. This package must depend on this
# subpackage to indirectly depend on these requirements.
Requires:       python3-%{name}+web = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:       python3-flask
Recommends:     python3-flask-cors

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
%if 0%{?rhel} && 0%{?rhel} <= 8
install-setup-generator
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
%endif

# empty configuration directory
install -d %{buildroot}%{_sysconfdir}/racksdb

# schema
install -d %{buildroot}%{_datadir}/racksdb
install -p -m 0644 schema/racksdb.yml %{buildroot}%{_datadir}/racksdb/schema.yml

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

%files -n %{name}-web
%{_bindir}/racksdb-web
%doc %{_mandir}/man1/racksdb-web.*

{{ changelog }}
