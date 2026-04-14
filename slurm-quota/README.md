# slurm-quota

Development packages:

```
fatbuildrctl --uri https://build.rackslab.io/devs build -a slurm-quota -d el9 --sources 1.9.0a1@.
```

Official releases:

```
export FATBUILDR_URI=https://build.rackslab.io/pkgs
export BUILD_MESSAGE="New upstream release v2.0.0"
export ARTIFACT=slurm-quota
fatbuildrctl build -a ${ARTIFACT} -m "${BUILD_MESSAGE}" -d el9
```