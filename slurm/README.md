# Slurm

Build Slurm packages for all supported versions on all supported distributions:

```sh
export SLURM_VERSIONS="23.11 24.05 24.11 25.05 25.11"
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
export SLURM_VERSIONS="23.11 24.05 24.11 25.05 25.11"
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

Remove empty distributions in repository:

```
sudo -u fatbuildr reprepro --basedir /var/lib/fatbuildr/registry/hpckit/deb clearvanished
```

```sh
export export FATBUILDR_URI=dbus://system/hpckit
export SLURM_VERSION=25.11
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm -d bookworm -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}

export export FATBUILDR_URI=dbus://system/hpckit
export SLURM_VERSION=25.05
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm -d bookworm -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}

export SLURM_VERSION=24.11
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm -d bookworm -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}

export SLURM_VERSION=24.05
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm -d bookworm -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}

export SLURM_VERSION=23.11
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm -d bookworm -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
```
