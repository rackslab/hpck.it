%?python_enable_dependency_generator

# This package supports both old setuptools way of building packages with the
# setup.py script provided in RFL build package on RHEL8 and the modern way with
# wheels and pyproject.toml on other systems with more recent versions of
# Python, pip, setuptools and Python RPM macros.

Name:           slurm-web
Version:        {{ version }}
Release:        {{ release }}
Summary:        Web dashboard for Slurm HPC workload manager

License:        GPLv3+
Group:          System Environment/Base
URL:            https://github.com/rackslab/slurm-web
{{ sources }}
{{ patches }}
BuildRequires:  python3-devel
%if 0%{?rhel}
BuildRequires:  python3-rfl-build
%endif
{% if pkg.distribution == "el8" %}
# On RHEL8, versions constraints must be set to ensure nodejs and npm are
# selected from nodejs:18 DNF module.
BuildRequires:  nodejs(engine) >= 18
BuildRequires:  npm(npm) >= 10
{% else %}
BuildRequires:  nodejs(engine)
BuildRequires:  npm
{% endif %}
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros

%description
Slurm-web is a web dashboard for Slurm workload manager on HPC clusters.

%if ! 0%{?rhel} || 0%{?rhel} >= 9
%generate_buildrequires
%if 0%{?rhel}
rfl-install-setup-generator > /dev/null
%endif
%pyproject_buildrequires -x agent
%endif

%package -n python3-%{name}
Summary:        Web dashboard for Slurm HPC workload manager: common backend library
BuildArch:      noarch
%description -n python3-%{name}
Slurm-web is a web dashboard for Slurm workload manager on HPC clusters.

This package contains the backend Python library used by gateway and agent
components.

%package -n %{name}-gateway
Summary:        Web dashboard for Slurm HPC workload manager: gateway
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
%description -n %{name}-gateway
Slurm-web is a web dashboard for Slurm workload manager on HPC clusters.

This package contains the backend gateway component and the frontend user
interface.

%package -n %{name}-agent
Summary:        Web dashboard for Slurm HPC workload manager: agent
BuildArch:      noarch
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3dist(racksdb[web])
Requires:       python3dist(redis)
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
%if 0%{?rhel}
rfl-install-setup-generator
%endif
%if 0%{?rhel} && 0%{?rhel} <= 8
%py3_build
%else
%pyproject_wheel
%endif

# Build frontend app
npm --prefix=frontend run build

%install
%if 0%{?rhel} && 0%{?rhel} <= 8
%py3_install
%else
%pyproject_install
%pyproject_save_files slurmweb
%endif

# Install vendor configuration files definitions
install -d %{buildroot}%{_datadir}/slurm-web
install -d %{buildroot}%{_datadir}/slurm-web/conf
install -p -m 0644 conf/vendor/* %{buildroot}%{_datadir}/slurm-web/conf/

# Install example WSGI scripts
install -d %{buildroot}%{_datadir}/slurm-web/wsgi
install -d %{buildroot}%{_datadir}/slurm-web/wsgi/gateway
install -d %{buildroot}%{_datadir}/slurm-web/wsgi/agent
install -p -m 0644 lib/wsgi/gateway/* %{buildroot}%{_datadir}/slurm-web/wsgi/gateway
install -p -m 0644 lib/wsgi/agent/* %{buildroot}%{_datadir}/slurm-web/wsgi/agent

# Move executables in libexec dedicated subdir
install -d %{buildroot}%{_libexecdir}/slurm-web
mv %{buildroot}%{_bindir}/* %{buildroot}%{_libexecdir}/slurm-web/

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

%if 0%{?rhel} && 0%{?rhel} <= 8
%define _pysuffix egg-info
%else
%define _pysuffix dist-info
%endif

# Except on RHEL8, try to import all modules to check dependencies.
%if !0%{?rhel} || 0%{?rhel} >= 9
%check
%pyproject_check_import
%endif

%files -n python3-%{name}
%license LICENSE
%doc README.md
%{python3_sitelib}/slurmweb/
%{python3_sitelib}/Slurm_web-*.%{_pysuffix}/
%{_sysconfdir}/slurm-web
%{_sharedstatedir}/slurm-web

%files -n %{name}-gateway
%{_libexecdir}/slurm-web/slurm-web-gateway
%{_libexecdir}/slurm-web/slurm-web-ldap-check
%{_libexecdir}/slurm-web/slurm-web-gen-jwt-key
%{_datadir}/slurm-web/frontend
%{_datadir}/slurm-web/wsgi/gateway
%{_datadir}/slurm-web/conf/gateway.yml
%{_sysusersdir}/slurm-web-gateway.conf
%{_unitdir}/slurm-web-gateway.service

%files -n %{name}-agent
%{_libexecdir}/slurm-web/slurm-web-agent
%{_datadir}/slurm-web/wsgi/agent
%{_datadir}/slurm-web/conf/agent.yml
%{_datadir}/slurm-web/conf/policy.yml
%{_datadir}/slurm-web/conf/policy.ini
%{_unitdir}/slurm-web-agent.service

%post -n %{name}-gateway
systemd-sysusers %{_sysusersdir}/slurm-web-gateway.conf

{{ changelog }}
