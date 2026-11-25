# Packages

FireHPC source produces these packages:

- `firehpc`: FireHPC CLI, Ansible configuration and plugins, OS images database.
- `firehpc-agent`: `firehpc-agent` program and system files (systemd services,
  wrappers, polkit rules, `firehpc` group) required on the host running the
  clusters containers. This is the only package required on remote hosts.
- `python3-firehpc`: FireHPC Python library shared by both packages.
- `firehpc-nvidia-fake`: fake `nvidia-smi` and DCGM exporter programs installed
  on emulated cluster GPU compute nodes. It does not depend on FireHPC library.

RPM packaging only produces `firehpc-nvidia-fake` package, for emulated cluster
nodes based on RHEL.

# Environments

Launch these commands to build the FireHPC environments:

```
$ export FATBUILDR_URI=https://build.rackslab.io/hpckit
$ fatbuildrctl build --artifact node-debian11 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl build --artifact node-debian12 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl build --artifact node-debian13 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl build --artifact node-debian14 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl build --artifact node-rocky8 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl build --artifact node-rocky9 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl build --artifact node-rocky10 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl build --artifact node-opensuse15 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl build --artifact node-opensuse16 --distribution firehpc --subdir firehpc/envs
```

## Rocky Linux 8

The `node-rocky8` image cannot be built anymore with the mkosi version used by
the builder (25.3). Upstream mkosi removed support of CentOS Stream 8 and EL8
variants, including Rocky Linux 8, as they reached end of life:

- Release notes: [mkosi NEWS](https://github.com/systemd/mkosi/blob/v24/NEWS.md#L172)
  (_Removed support for CentOS 8 Stream as it is now EOL_, listed in v23
  section, first enforced in tagged release v23.1).
- Check that refuses to build:
  [`mkosi/distributions/centos.py`](https://github.com/systemd/mkosi/blob/v25.3/mkosi/distributions/centos.py#L65-L66),
  inherited by the Rocky Linux installer. The build fails with:

  ```
  ‣ Rocky Linux Stream 8 or earlier variants are not supported
  ```

The published `node-rocky8_1.raw.xz` image was built with an older mkosi
(definitions updated for mkosi 22, image last changed in November 2024) and is
not updated anymore.

Removing this check is not enough to restore support with mkosi 25.3. It was
tested that these additional changes are also required:

- Use `PowerTools` repository instead of `CRB` on EL8, as `CRB` does not exist
  on Rocky Linux 8 (`mirrorlist?repo=CRB-8` returns 404).
- Extend the rpm-sequoia policy that mkosi writes for EL9 to EL8, to accept
  SHA1 signatures of EPEL 8 GPG key (`Key import failed (code 2)` otherwise).

These changes are not maintained as mkosi package patches and Rocky Linux 8 is
not tested anymore.

Known issue with the published image: systemd 239 in Rocky Linux 8 defaults to
`DNSSEC=allow-downgrade` in systemd-resolved, which makes DNS lookups fail in
FireHPC containers (`DNSSEC validation failed: missing-key`). Workaround in
running containers:

```
# mkdir -p /etc/systemd/resolved.conf.d
# printf '[Resolve]\nDNSSEC=no\n' > /etc/systemd/resolved.conf.d/firehpc.conf
# systemctl restart systemd-resolved
```
