#!/bin/sh
# Example SuspendProgram for cluster where every node has two CPUs
srun --uid=0 --no-allocate --nodelist=$1 echo powersave >/sys/devices/system/cpu0/cpufreq
srun --uid=0 --no-allocate --nodelist=$1 echo powersave >/sys/devices/system/cpu1/cpufreq
