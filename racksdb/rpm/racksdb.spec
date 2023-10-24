%?python_enable_dependency_generator

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
Requires:       python3-flask

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
%endif
%py3_build
make -C docs man

%install
%py3_install

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

%files
%{_bindir}/racksdb
%doc %{_mandir}/man1/racksdb.*

%files -n python3-%{name}
%license LICENSE
%doc README.md
%doc examples
%{python3_sitelib}/racksdb/
%{python3_sitelib}/RacksDB-*.egg-info/
%{_sysconfdir}/racksdb
%{_datadir}/racksdb
%{_sharedstatedir}/racksdb

%files -n %{name}-web
%{_bindir}/racksdb-web
%doc %{_mandir}/man1/racksdb-web.*

{{ changelog }}
