# Packages

TDB

# Environments

Launch these commands to build the FireHPC environments:

```
$ fatbuildrctl --uri dbus://system/hpckit build --artifact node-debian11 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl --uri dbus://system/hpckit build --artifact node-debian12 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl --uri dbus://system/hpckit build --artifact node-debian13 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl --uri dbus://system/hpckit build --artifact node-debian14 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl --uri dbus://system/hpckit build --artifact node-rocky8 --distribution firehpc --subdir firehpc/envs
$ fatbuildrctl --uri dbus://system/hpckit build --artifact node-rocky9 --distribution firehpc --subdir firehpc/envs
```

Export to remote repository:

```
$ rsync --rsync-path="sudo rsync"  -e "ssh -p 3322" -avh --delete /var/lib/fatbuildr/registry/hpckit roohatch@hpck.it:/var/lib/fatbuildr/registry/
```
