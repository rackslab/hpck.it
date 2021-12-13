#!/bin/sh
# Example ResumeProgram for cluster where every node has two CPUs
srun --uid=0 --no-allocate --nodelist=$1 echo performance >/sys/devices/system/cpu0/cpufreq
srun --uid=0 --no-allocate --nodelist=$1 echo performance >/sys/devices/system/cpu1/cpufreq

