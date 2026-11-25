%{?python_enable_dependency_generator}

# FireHPC CLI and agent are not packaged for RPM based distributions. This
# package only produces firehpc-nvidia-fake subpackage, built from the
# standalone Python project in utils/nvidia-fake/ subdirectory of FireHPC
# sources, to be installed on emulated cluster nodes. The main package has no
# %%files section, then it is not produced.
#
# This subpackage supports both old setuptools way of building packages with
# the setup.py script provided in RFL build package on RHEL8 and the modern way
# with wheels and pyproject.toml on other systems with more recent versions of
# Python, pip, setuptools and Python RPM macros.

Name:           firehpc
Version:        {{ version }}
Release:        {{ release }}
Summary:        Deploy container-based emulated HPC clusters

License:        GPL-3.0-or-later
URL:            https://github.com/rackslab/firehpc
{{ sources }}
{{ patches }}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-rfl-build
BuildRequires:  systemd-rpm-macros
{% if pkg.distribution == "el8" %}
BuildRequires:  python3-setuptools
{% endif %}

%description
FireHPC is an open source solution to deploy container-based emulated HPC
clusters, typically for development, testing or learning purposes.

%package nvidia-fake
Summary:        Fake NVIDIA tools for FireHPC emulated GPU nodes
BuildArch:      noarch

%description nvidia-fake
FireHPC is an open source solution to deploy container-based emulated HPC
clusters, typically for development, testing or learning purposes.

This package provides fake nvidia-smi and NVIDIA DCGM exporter programs to
emulate NVIDIA GPUs on emulated cluster compute nodes, for GPU monitoring tools
such as CEEMS exporter. It does not depend on FireHPC library and it is meant
to be installed on cluster nodes.

{# %pyproject_buildrequires macro is not supported on el8 #}
{% if pkg.distribution != "el8" %}
%generate_buildrequires
cd utils/nvidia-fake
{% if pkg.distribution == "el9" %}
rfl-install-setup-generator > /dev/null
{% endif %}
%pyproject_buildrequires
{% endif %}

%prep
{{ prep_sources }}
{{ prep_patches }}

%build
cd utils/nvidia-fake
{% if pkg.distribution in ["el8", "el9"] %}
# Setuptools is too old to support PEP 621 metadata in pyproject.toml on these
# distributions, generate setup.py script with RFL build.
rfl-install-setup-generator
{% endif %}
{% if pkg.distribution == "el8" %}
%py3_build
{% else %}
%pyproject_wheel
{% endif %}

%install
cd utils/nvidia-fake
{% if pkg.distribution == "el8" %}
%py3_install
{% else %}
%pyproject_install
{% endif %}
install -Dm0644 systemd/firehpc-dcgm-exporter.service \
    %{buildroot}%{_unitdir}/firehpc-dcgm-exporter.service

{% if pkg.distribution == "el8" %}
%define _nvidia_fake_pysuffix egg-info
{% else %}
%define _nvidia_fake_pysuffix dist-info
{% endif %}

%check
# Unit tests require prometheus_client, only check modules can be imported.
PYTHONPATH=%{buildroot}%{python3_sitelib} %{python3} -c \
    'import firehpc_nvidia_fake.smi, firehpc_nvidia_fake.dcgm'

%post nvidia-fake
%systemd_post firehpc-dcgm-exporter.service

%preun nvidia-fake
%systemd_preun firehpc-dcgm-exporter.service

%postun nvidia-fake
%systemd_postun_with_restart firehpc-dcgm-exporter.service

%files nvidia-fake
%license LICENSE
%doc utils/nvidia-fake/README.md
%{_bindir}/firehpc-nvidia-smi
%{_bindir}/firehpc-dcgm-exporter
%{python3_sitelib}/firehpc_nvidia_fake/
%{python3_sitelib}/firehpc_nvidia_fake-*.%{_nvidia_fake_pysuffix}/
%{_unitdir}/firehpc-dcgm-exporter.service

{{ changelog }}
