# Slurm

Build Slurm packages for all supported versions on all supported distributions:

```sh
export SLURM_VERSIONS="23.02 23.11 24.05"
export SLURM_DISTRIBS="bookworm trixie sid el8 el9"
for SLURM_DISTRIB in ${SLURM_DISTRIBS}; do
  for SLURM_VERSION in ${SLURM_VERSIONS}; do
    fatbuildrctl --uri dbus://system/hpckit build -a slurm -d ${SLURM_DISTRIB} --derivative slurm${SLURM_VERSION} --batch
  done
done
```

Clean repositories of all Slurm packages for all supported version and all
supported distributions:

```sh
export SLURM_VERSIONS="23.02 23.11 24.05"
export SLURM_DISTRIBS="bookworm trixie sid el8 el9"
export SLURM_ARTIFACTS="pmi sack slurm sview"
for SLURM_ARTIFACT in ${SLURM_ARTIFACTS}; do
  for SLURM_DISTRIB in ${SLURM_DISTRIBS}; do
    for SLURM_VERSION in ${SLURM_VERSIONS}; do
      fatbuildrctl --uri dbus://system/hpckit registry -a ${SLURM_ARTIFACT} -d ${SLURM_DISTRIB} --derivative slurm${SLURM_VERSION} delete
    done
  done
done
```
