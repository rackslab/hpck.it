%{?python_enable_dependency_generator}

Name:           slurm-quota
Version:        {{ version }}
Release:        {{ release }}
Summary:        Slurm quota management tool

License:        GPL-2.0-or-later
URL:            https://github.com/rackslab/slurm-quota
{{ sources }}
{{ patches }}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-rfl-build
BuildRequires:  asciidoctor
BuildRequires:  bash-completion
BuildRequires:  systemd-rpm-macros
Requires:       python3-%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
slurm-quota assigns CPU/GPU minute quotas to Slurm users and accounts and
enforces them on submission and completion paths.

This package contains the user CLI for compute and login nodes.

%generate_buildrequires
rfl-install-setup-generator > /dev/null
%pyproject_buildrequires -x dev -x serve -x web

%pyproject_extras_subpkg -n python3-%{name} serve
%pyproject_extras_subpkg -n python3-%{name} web

%package -n python3-%{name}
Summary:        Slurm quota management tool: Python library
BuildArch:      noarch

%description -n python3-%{name}
slurm-quota assigns CPU/GPU minute quotas to Slurm users and accounts and
enforces them on submission and completion paths.

This package contains the Python library.

%package controller
Summary:        Controller-side files for slurm-quota
Requires:       python3-%{name}+serve = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       lua-dbi
Requires:       lua-posix
Requires:       sqlite

%description controller
Controller package for slurm-quota with Slurm integration files, systemd units,
logrotate policy and database migration.

%package web
Summary:        Web dashboard for slurm-quota
Requires:       python3-%{name}+web = %{?epoch:%{epoch}:}%{version}-%{release}

%description web
Web dashboard package for slurm-quota. It provides the `slurm-quota-web` Flask
WSGI application and static/template assets. It can run standalone with Flask's
built-in server for testing, or behind Apache/mod_wsgi in production.

%prep
{{ prep_sources }}
{{ prep_patches }}

%build
rfl-install-setup-generator
%pyproject_wheel

# Rewrite /usr/local/bin references to libexec paths for internal commands
sed -i 's|/usr/local/bin/slurm-quota-charge|%{_libexecdir}/slurm-quota/slurm-quota-charge|g' slurm-quota-charge-wrapper
sed -i 's|/usr/local/bin/slurm-quota-serve|%{_libexecdir}/slurm-quota/slurm-quota-serve|g' slurm-quota.service

# Generate man pages from source AsciiDoc files.
asciidoctor -a revnumber=%{version} -b manpage -o slurm-quota.1 man/slurm-quota.1.adoc
asciidoctor -a revnumber=%{version} -b manpage -o slurm-quota-charge.1 man/slurm-quota-charge.1.adoc
asciidoctor -a revnumber=%{version} -b manpage -o slurm-quota-serve.1 man/slurm-quota-serve.1.adoc
asciidoctor -a revnumber=%{version} -b manpage -o slurm-quota-token.1 man/slurm-quota-token.1.adoc
asciidoctor -a revnumber=%{version} -b manpage -o slurm-quota-prune.1 man/slurm-quota-prune.1.adoc
asciidoctor -a revnumber=%{version} -b manpage -o slurm-quota-web.1 man/slurm-quota-web.1.adoc

%install
%pyproject_install
%pyproject_save_files slurm_quota

# RFL.build installs data-files under %{_prefix}/slurm-quota; relocate to %{_datadir}
install -d %{buildroot}%{_datadir}
mv %{buildroot}%{_prefix}/slurm-quota %{buildroot}%{_datadir}/

# Default environment file for web service
install -Dm0644 %{buildroot}%{_datadir}/slurm-quota/conf/slurm-quota-web.default \
    %{buildroot}%{_sysconfdir}/default/slurm-quota-web
rm -f %{buildroot}%{_datadir}/slurm-quota/conf/slurm-quota-web.default

# Site configuration for REST API
install -Dm0644 %{buildroot}%{_datadir}/slurm-quota/conf/serve.ini.example \
    %{buildroot}%{_sysconfdir}/slurm-quota/serve.ini
rm -f %{buildroot}%{_datadir}/slurm-quota/conf/serve.ini.example

# Move internal commands out of bindir (not intended for end users)
install -d %{buildroot}%{_libexecdir}/slurm-quota
mv %{buildroot}%{_bindir}/slurm-quota-charge %{buildroot}%{_libexecdir}/slurm-quota/
mv %{buildroot}%{_bindir}/slurm-quota-serve %{buildroot}%{_libexecdir}/slurm-quota/
mv %{buildroot}%{_bindir}/slurm-quota-migrate %{buildroot}%{_libexecdir}/slurm-quota/
mv %{buildroot}%{_bindir}/slurm-quota-web %{buildroot}%{_libexecdir}/slurm-quota/

# Slurm integration and systemd units
install -Dm0755 slurm-quota-charge-wrapper %{buildroot}%{_sysconfdir}/slurm/slurm-quota-charge-wrapper
install -Dm0644 job_submit.lua %{buildroot}%{_sysconfdir}/slurm/job_submit.lua
install -Dm0644 slurm-quota.service %{buildroot}%{_unitdir}/slurm-quota.service
install -Dm0644 slurm-quota.socket %{buildroot}%{_unitdir}/slurm-quota.socket
install -Dm0644 slurm-quota-charge.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/slurm-quota-charge

# Site configuration directory
install -d %{buildroot}%{_sysconfdir}/slurm-quota

# Bash completion
install -Dm0644 slurm-quota.bash-completion %{buildroot}%{bash_completions_dir}/slurm-quota
install -Dm0644 slurm-quota-prune.bash-completion %{buildroot}%{bash_completions_dir}/slurm-quota-prune
install -Dm0644 slurm-quota-token.bash-completion %{buildroot}%{bash_completions_dir}/slurm-quota-token

# Man pages
install -Dm0644 slurm-quota.1 %{buildroot}%{_mandir}/man1/slurm-quota.1
install -Dm0644 slurm-quota-charge.1 %{buildroot}%{_mandir}/man1/slurm-quota-charge.1
install -Dm0644 slurm-quota-serve.1 %{buildroot}%{_mandir}/man1/slurm-quota-serve.1
install -Dm0644 slurm-quota-token.1 %{buildroot}%{_mandir}/man1/slurm-quota-token.1
install -Dm0644 slurm-quota-prune.1 %{buildroot}%{_mandir}/man1/slurm-quota-prune.1
install -Dm0644 slurm-quota-web.1 %{buildroot}%{_mandir}/man1/slurm-quota-web.1

# State and log directories
install -d %{buildroot}%{_localstatedir}/log/slurm/charge
install -d %{buildroot}%{_sharedstatedir}/state/slurm-quota

%define _slurm_quota_pysuffix dist-info

%check
%pyproject_check_import -e 'slurm_quota.tests*'
%pytest

%post controller
DB_PATH=%{_sharedstatedir}/state/slurm-quota/slurm-quota.db
MIGRATE=%{_libexecdir}/slurm-quota/slurm-quota-migrate

if [ -x "${MIGRATE}" ] && [ -f "${DB_PATH}" ]; then
    "${MIGRATE}" || exit 1
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/slurm-quota
%{bash_completions_dir}/slurm-quota
%doc %{_mandir}/man1/slurm-quota.1*

%files -n python3-%{name}
%{python3_sitelib}/slurm_quota/
%{python3_sitelib}/*-*.%{_slurm_quota_pysuffix}/

%files controller
%dir %{_datadir}/slurm-quota/conf
%{_datadir}/slurm-quota/conf/serve.yml
%dir %{_sysconfdir}/slurm-quota
%config(noreplace) %{_sysconfdir}/slurm-quota/serve.ini
%{_libexecdir}/slurm-quota/slurm-quota-charge
%{_libexecdir}/slurm-quota/slurm-quota-serve
%{_libexecdir}/slurm-quota/slurm-quota-migrate
%{_bindir}/slurm-quota-token
%{_bindir}/slurm-quota-prune
%doc %{_mandir}/man1/slurm-quota-charge.1*
%doc %{_mandir}/man1/slurm-quota-serve.1*
%doc %{_mandir}/man1/slurm-quota-token.1*
%doc %{_mandir}/man1/slurm-quota-prune.1*
%{bash_completions_dir}/slurm-quota-prune
%{bash_completions_dir}/slurm-quota-token
%{_sysconfdir}/slurm/slurm-quota-charge-wrapper
%config(noreplace) %{_sysconfdir}/slurm/job_submit.lua
%{_unitdir}/slurm-quota.service
%{_unitdir}/slurm-quota.socket
%config(noreplace) %{_sysconfdir}/logrotate.d/slurm-quota-charge
%dir %attr(0755,slurm,slurm) %{_localstatedir}/log/slurm/charge
%dir %attr(0755,slurm,slurm) %{_sharedstatedir}/state/slurm-quota

%files web
%{_libexecdir}/slurm-quota/slurm-quota-web
%{_datadir}/slurm-quota/web/
%config(noreplace) %{_sysconfdir}/default/slurm-quota-web
%doc %{_mandir}/man1/slurm-quota-web.1*

{{ changelog }}
