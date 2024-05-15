# Quantum Espresso workflow tool: `qeflow`

[![GitHub Release Date](https://img.shields.io/github/release-date/t3n0/qeflow)](latest)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/t3n0/qeflow)](latest)
[![GitHub all releases](https://img.shields.io/github/downloads/t3n0/qeflow/total)](latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](gpl3)

QE-flow is a python tool which helps to automate quantum espresso workflows "without scassamento di maroni", i.e. *easily*.
Out in the internet there are many other options that perform this very same tasks and in a much more efficient way.
The most notable are [pwtk](http://pwtk.ijs.si/index.html) and [aiida](https://aiida-quantumespresso.readthedocs.io/en/latest/).
However, in my opinion, these tools have a very steap learning curve. So I decided to just write my own.

## Installation

Simply download the [latest version](download) and run

```bash
pip install qeflow-X.Y.tar.gz
```

where you must replace `X.Y` with the version you have downloaded.
In the future, if this project keeps growing, I'll try to upload qeflow to [PyPI](https://pypi.org/).

## Quick start

QE-flow is meant to be easy. We only need to setup 2 files:

1. a very small configuration file (once and for all),
2. and an input file with the workflow instructions.

Note that the input file is very easy to setup: it is mostly a collection of the usual well known QE flags plus the workflow instructions.

### 1. Configuration file

The first thing to do is to create a configuration file. QE-flow will try to read the configuration file in the following order:

1. from `./qeflow.cfg` (in the current directory)
2. or from `$HOME/.qeflow.cfg` (notice the dot, hidden file)

A configuration file skeleton is found in [qeflowSkel.cfg](examples/qeflowSkel.cfg). In the following we show 2 examples.

1. **Local** configuration: useful we running simulation on a personal computer.

    ```yaml
    # $HOME/.qeflow.cfg
    cluster: local
    pwx: path/to/pw.x
    mpix: path/to/mpirun
    ```

2. **Slurm** configuration: this is necessary when we are logged in a HPC facility with a slurm batch system.

    ```yaml
    # $HOME/.qeflow.cfg
    cluster: slurm
    cores_per_node: 128
    account: account-name
    pyenv: /path/to/python/env/bin/activate
    modules:
        - quantum-espresso-7.1
    pwx: pw.x
    mpix: mpirun
    ```

In the future, I might implement also the PBS batch system.

### 2. Input file

The input file skeleton with the currently supported flags and relative description is found in [qeflowSkel.in](examples/qeflowSkel.in).
In the following I'll show only a minimal example: 


[gpl3]: https://www.gnu.org/licenses/gpl-3.0
[latest]: https://github.com/t3n0/qeflow/releases/latest
[download]: https://github.com/t3n0/qeflow/releases/download/v0.1/qeflow-v0.1.zip