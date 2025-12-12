%{?python_enable_dependency_generator}

# This package supports both old setuptools way of building packages with the
# setup.py script provided in RFL build package on RHEL8 and the modern way with
# wheels and pyproject.toml on other systems with more recent versions of
# Python, pip, setuptools and Python RPM macros.

Name:           slurm-web
Version:        {{ version }}
Release:        {{ release }}
Summary:        Web dashboard for Slurm HPC workload manager

License:        MIT
Group:          System Environment/Base
URL:            https://github.com/rackslab/slurm-web
{{ sources }}
{{ patches }}
BuildRequires:  python3-devel
BuildRequires:  python3-rfl-build
{% if pkg.distribution == "el8" %}
# On RHEL8, versions constraints must be set to ensure nodejs and npm are
# selected from nodejs:18 DNF module.
BuildRequires:  nodejs(engine) >= 18
BuildRequires:  npm(npm) >= 10
{% else %}
BuildRequires:  nodejs(engine)
BuildRequires:  npm
{% endif %}
{% if pkg.distribution == "el8" %}
# PyYAML library is required for docs/update-materials script. It does not have
# to be explicitely declared as build requirement except on el8 because it is
# also a build requirement of Slurm-web itself and is automatically detected and
# declared by pyproject_buildrequires macro on other distributions.
BuildRequires:  python3-pyyaml
{% elif pkg.distribution in ["suse15", "suse16"] %}
BuildRequires:  python-rpm-macros
BuildRequires:  python-rpm-generators
BuildRequires:  fdupes
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
# pyproject_buildrequires macro is not supported on openSUSE, build and tests
# dependencies must be explicitely declared for these distributions.
BuildRequires:  python3-PyYAML
BuildRequires:  python3-aiohttp
BuildRequires:  python3-clustershell
BuildRequires:  python3-Flask
BuildRequires:  python3-rfl-authentication
BuildRequires:  python3-rfl-core
BuildRequires:  python3-rfl-log
BuildRequires:  python3-rfl-settings
BuildRequires:  python3-rfl-web
BuildRequires:  python3-Markdown
BuildRequires:  python3-parameterized
BuildRequires:  python3-prometheus-client
BuildRequires:  python3-pytest
BuildRequires:  python3-racksdb-web
BuildRequires:  python3-redis
BuildRequires:  python3-requests
{% endif %}
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
{% if pkg.distribution == "suse15" %}
BuildRequires:  ruby2.5-rubygem-asciidoctor
{% elif pkg.distribution == "suse16" %}
BuildRequires:  ruby3.4-rubygem-asciidoctor
{% else %}
BuildRequires:  asciidoctor
{% endif %}

%description
Slurm-web is a web dashboard for Slurm workload manager on HPC clusters.

{# %pyproject_buildrequires macro is not supported on el8 and suse #}
{% if pkg.distribution not in ["el8", "suse15", "suse16"] %}
%generate_buildrequires
%if 0%{?rhel}
rfl-install-setup-generator > /dev/null
%endif
%pyproject_buildrequires -x agent -x gateway -x tests
{% endif %}

%package -n python3-%{name}
Summary:        Web dashboard for Slurm HPC workload manager: common backend library
BuildArch:      noarch
{% if pkg.distribution == "el8" %}
# Slurm-web tries to import importlib_metadata from functools which is available
# starting from Python >= 3.8, and fallback to compatible external dependency
# otherwise. This optional dependency is not declared in pyproject.toml, because
# it is not required in most cases. Then it must be defined explicitely here for
# el8 with Python 3.6.
Requires:       python3dist(importlib-metadata)
{% elif pkg.distribution == "suse15" %}
# Automatic dependency generator does not work on suse15, dependencies must be
# explicitely declared for this distribution.
Requires:       python3-aiohttp
Requires:       python3-Flask
Requires:       python3-rfl-authentication
Requires:       python3-rfl-core
Requires:       python3-rfl-log
Requires:       python3-rfl-settings
Requires:       python3-rfl-web
# Slurm-web tries to import importlib_metadata from functools which is available
# starting from Python >= 3.8, and fallback to compatible external dependency
# otherwise. This optional dependency is not declared in pyproject.toml, because
# it is not required in most cases. Then it must be defined explicitely here for
# suse15 with Python 3.6.
Requires:       python3-importlib-metadata
{% endif %}

%description -n python3-%{name}
Slurm-web is a web dashboard for Slurm workload manager on HPC clusters.

This package contains the backend Python library used by gateway and agent
components.

%package -n %{name}-gateway
Summary:        Web dashboard for Slurm HPC workload manager: gateway
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
{% if pkg.distribution in ["suse15", "suse16"] %}
Requires:       python3-Markdown
{% else %}
Requires:       python3dist(markdown)
{% endif %}
%description -n %{name}-gateway
Slurm-web is a web dashboard for Slurm workload manager on HPC clusters.

This package contains the backend gateway component and the frontend user
interface.

%package -n %{name}-agent
Summary:        Web dashboard for Slurm HPC workload manager: agent
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
{% if pkg.distribution in ["suse15", "suse16"] %}
Requires:       python3-clustershell
Requires:       python3-prometheus-client
Requires:       python3-racksdb-web
Requires:       python3-redis
Requires:       python3-requests
{% else %}
Requires:       python3dist(clustershell)
Requires:       python3dist(prometheus-client)
Requires:       python3dist(racksdb[web])
Requires:       python3dist(redis)
Requires:       python3dist(requests)
{% endif %}
Suggests:       racksdb
Suggests:       slurm-slurmrestd
Suggests:       redis
%description -n %{name}-agent
Slurm-web is a web dashboard for Slurm workload manager on HPC clusters.

This package contains the backend agent component.

%global debug_package %{nil}

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

# Build frontend app
npm --prefix=frontend run build

# Generate manpages
docs/update-materials man

%install
{% if pkg.distribution == "el8" %}
%py3_install
{% else %}
%pyproject_install
{% if pkg.distribution not in ["suse15", "suse16"] %}
%pyproject_save_files slurmweb
{% endif %}
{% endif %}

{% if pkg.distribution in ["suse15", "suse16"] %}
%python_expand %fdupes %{buildroot}%{$python_sitelib}
{% endif %}

# Install vendor configuration files definitions
install -d %{buildroot}%{_datadir}/slurm-web
install -d %{buildroot}%{_datadir}/slurm-web/conf
install -d %{buildroot}%{_datadir}/slurm-web/templates
install -p -m 0644 conf/vendor/*.{yml,ini} %{buildroot}%{_datadir}/slurm-web/conf/
install -p -m 0644 conf/vendor/templates/* %{buildroot}%{_datadir}/slurm-web/templates/

# Install example WSGI scripts
install -d %{buildroot}%{_datadir}/slurm-web/wsgi
install -d %{buildroot}%{_datadir}/slurm-web/wsgi/gateway
install -d %{buildroot}%{_datadir}/slurm-web/wsgi/agent
install -p -m 0644 lib/wsgi/gateway/* %{buildroot}%{_datadir}/slurm-web/wsgi/gateway
install -p -m 0644 lib/wsgi/agent/* %{buildroot}%{_datadir}/slurm-web/wsgi/agent

# Move executables in libexec dedicated subdir
install -d %{buildroot}%{_libexecdir}/slurm-web
{% if pkg.version.major | int < 6 %}
mv %{buildroot}%{_bindir}/* %{buildroot}%{_libexecdir}/slurm-web/
{% else %}
install -p -m 0755 lib/exec/slurm-web-compat %{buildroot}%{_libexecdir}/slurm-web/
ln -s slurm-web-compat %{buildroot}%{_libexecdir}/slurm-web/slurm-web-agent
ln -s slurm-web-compat %{buildroot}%{_libexecdir}/slurm-web/slurm-web-connect-check
ln -s slurm-web-compat %{buildroot}%{_libexecdir}/slurm-web/slurm-web-gateway
ln -s slurm-web-compat %{buildroot}%{_libexecdir}/slurm-web/slurm-web-gen-jwt-key
ln -s slurm-web-compat %{buildroot}%{_libexecdir}/slurm-web/slurm-web-ldap-check
ln -s slurm-web-compat %{buildroot}%{_libexecdir}/slurm-web/slurm-web-show-conf
{% endif %}

# Install frontend application in datadir
cp -vdr --no-preserve=ownership frontend/dist %{buildroot}%{_datadir}/slurm-web/frontend

# Empty configuration directory
install -d %{buildroot}%{_sysconfdir}/slurm-web

# Empty shared state directory
install -d %{buildroot}%{_sharedstatedir}/slurm-web

# Install systemd units
install -p -D -m 0644 lib/systemd/* -t %{buildroot}%{_unitdir}

# Install sysuser conf
install -p -D -m 0644 lib/sysusers/* -t %{buildroot}%{_sysusersdir}

# Install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 0644 docs/man/*.1 %{buildroot}%{_mandir}/man1/

# Install configuration examples
install -d %{buildroot}%{_docdir}/slurm-web-gateway/examples
install -d %{buildroot}%{_docdir}/slurm-web-agent/examples
install -p -m 0644 docs/modules/conf/examples/gateway.ini %{buildroot}%{_docdir}/slurm-web-gateway/examples
install -p -m 0644 docs/modules/conf/examples/agent.ini %{buildroot}%{_docdir}/slurm-web-agent/examples

{% if pkg.distribution == "el8" %}
%define _pysuffix egg-info
{% else %}
%define _pysuffix dist-info
{% endif %}

{% if pkg.distribution != "el8" %}
%check
{% if pkg.distribution not in ["suse15", "suse16"] %}
# Except on RHEL8 and openSUSE where it is not supported, run
# pyproject_check_import on all packages modules.
%pyproject_check_import -e 'slurmweb.tests*'
{% endif %}
# Run pytest to execute unit tests, except on RHEL8 because testing dependencies
# are not automatically installed by generate_buildrequires macro on this
# distribution.
%pytest
{% endif %}

%files -n python3-%{name}
%license LICENSE
%doc README.md
{% if pkg.version.major | int > 5 %}
%doc %{_mandir}/man1/slurm-web.*
{% endif %}
%doc %{_mandir}/man1/slurm-web-show-conf.*
%{python3_sitelib}/slurmweb/
%{python3_sitelib}/*-*.%{_pysuffix}/
%{_sysconfdir}/slurm-web
{% if pkg.version.major | int > 5 %}
%{_bindir}/slurm-web
{% endif %}
{% if pkg.version.major | int > 5 %}
%{_libexecdir}/slurm-web/slurm-web-compat
{% endif %}
%{_libexecdir}/slurm-web/slurm-web-show-conf
%{_sysusersdir}/slurm-web.conf
%{_sharedstatedir}/slurm-web

%files -n %{name}-gateway
%doc %{_mandir}/man1/slurm-web-gateway.*
%doc %{_mandir}/man1/slurm-web-ldap-check.*
%doc %{_mandir}/man1/slurm-web-gen-jwt-key.*
%doc %{_docdir}/slurm-web-gateway/examples/gateway.ini
%{_libexecdir}/slurm-web/slurm-web-gateway
%{_libexecdir}/slurm-web/slurm-web-ldap-check
%{_libexecdir}/slurm-web/slurm-web-gen-jwt-key
%{_datadir}/slurm-web/frontend
%{_datadir}/slurm-web/wsgi/gateway
%{_datadir}/slurm-web/conf/gateway.yml
%{_datadir}/slurm-web/templates
%{_unitdir}/slurm-web-gateway.service

%files -n %{name}-agent
%doc %{_mandir}/man1/slurm-web-agent.*
%doc %{_mandir}/man1/slurm-web-connect-check.*
%doc %{_docdir}/slurm-web-agent/examples/agent.ini
%{_libexecdir}/slurm-web/slurm-web-agent
%{_libexecdir}/slurm-web/slurm-web-connect-check
%{_datadir}/slurm-web/wsgi/agent
%{_datadir}/slurm-web/conf/agent.yml
%{_datadir}/slurm-web/conf/policy.yml
%{_datadir}/slurm-web/conf/policy.ini
%{_unitdir}/slurm-web-agent.service

%post -n python3-%{name}
systemd-sysusers %{_sysusersdir}/slurm-web.conf

{{ changelog }}
