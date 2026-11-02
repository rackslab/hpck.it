# Slurm emulator

## Slurm 26.05

Build packkages for Slurm 26.05:

``̀ sh
export FATBUILDR_URI=https://build.rackslab.io/hpckit
export SLURM_VERSION=26.05
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
#fatbuildrctl build -a slurm-emulator -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION} # fails with PMIx 7?
fatbuildrctl build -a slurm-emulator -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION} # fails with PMIx 7?
fatbuildrctl build -a slurm-emulator -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el10 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
```

## Slurm 25.11

Build packkages for Slurm 25.11:

``̀ sh
export FATBUILDR_URI=https://build.rackslab.io/hpckit
export SLURM_VERSION=25.11
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm-emulator -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el10 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
```

## Slurm 25.05

Build packkages for Slurm 25.05:

``̀ sh
export FATBUILDR_URI=https://build.rackslab.io/hpckit
export SLURM_VERSION=25.05
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm-emulator -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el10 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
```

## Slurm 24.11

Build packkages for Slurm 24.11:

``̀ sh
export FATBUILDR_URI=https://build.rackslab.io/hpckit
export SLURM_VERSION=24.11
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm-emulator -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el10 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
```

## Slurm 24.05

Build packkages for Slurm 24.05:

``̀ sh
export FATBUILDR_URI=https://build.rackslab.io/hpckit
export SLURM_VERSION=24.11
export BUILD_MESSAGE="New upstream release ${SLURM_VERSION}"
fatbuildrctl build -a slurm-emulator -d trixie -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d forky -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d sid -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el8 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el9 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
fatbuildrctl build -a slurm-emulator -d el10 -m "${BUILD_MESSAGE}" --derivative slurm${SLURM_VERSION}
```