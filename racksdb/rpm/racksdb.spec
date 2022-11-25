%?python_enable_dependency_generator

Name:           racksdb
Version:	{{ version }}
Release:	{{ release }}
Summary:        YAML database of datacenter infrastructures

License:        GPLv3+
Group:          System Environment/Base
URL:            https://github.com/rackslab/racksdb
{{ source }}
{{ patches }}
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  make
BuildRequires:  asciidoctor

%description
RacksDB is an open source solution to modelize your datacenters infrastructures
in a simple YAML-based database to store information about the equipments in
your datacenters provided with tools and library to request this database.

%prep
{{ prep_sources }}
{{ prep_patches }}

%build
%py3_build
make -C docs man

%install
%py3_install

# empty configuration directory
install -d %{buildroot}%{_sysconfdir}/racksdb

# schema
install -d %{buildroot}%{_datadir}/racksdb
install -p -m 0644 schema/racksdb.yml %{buildroot}/%{_datadir}/racksdb/schema.yml

# empty database directory
install -d %{buildroot}%{_sharedstatedir}/racksdb

# man pages
install -d %{buildroot}/%{_mandir}/man1
install -p -m 0644 docs/man/*.1 %{buildroot}/%{_mandir}/man1/

%files
%license LICENSE
%doc README.md
%doc examples
%{python3_sitelib}/racksdb/
%{python3_sitelib}/RacksDB-*.egg-info/
%{_sysconfdir}/racksdb
%{_bindir}/racksdb
%{_datadir}/racksdb
%{_sharedstatedir}/racksdb
%doc %{_mandir}/man1/*


{{ changelog }}
