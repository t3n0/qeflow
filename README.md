# `qeflow` Quantum Espresso workflow tool

[![GitHub Release Date](https://img.shields.io/github/release-date/t3n0/qeflow)](https://github.com/t3n0/qeflow/releases/latest)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/t3n0/qeflow)](https://github.com/t3n0/qeflow/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/t3n0/qeflow/total)](https://github.com/t3n0/qeflow/releases/latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

QE-flow is a python tool which helps to automate quantum espresso workflows "without scassamento di maroni", i.e. *easily*.
Out in the internet there are many other options that perform this very same tasks and in a much more efficient way.
The most notable are [pwtk](http://pwtk.ijs.si/index.html) and [aiida](https://aiida-quantumespresso.readthedocs.io/en/latest/).
However, in my opinion, these tools have a very steap learning curve. So I decided to just write my own.

## Installation

Simply download the [latest version](https://github.com/t3n0/qeflow/releases/download/v0.1/qeflow-0.1.tar.gz) and run

```bash
pip install qeflow-X.Y.tar.gz
```

where you must replace `X.Y` with the version you have downloaded.
In the future, if this project keeps growing, I'll try to upload qeflow to [PyPI](https://pypi.org/).

## Quick start

QE-flow is meant to be easy. We only need to setup 2 files:

1. a very small **configuration file** (once and for all),
2. and an **input file** with the workflow instructions.

Note that the input file is very easy to setup: it is mostly a collection of the usual well known QE flags plus the workflow instructions.

### 1. Configuration file

The first thing to do is to create a configuration file. QE-flow will try to read the configuration file in the following order:

1. from `./qeflow.cfg` (in the current directory)
2. or from `$HOME/.qeflow.cfg` (notice the dot, hidden file)

A configuration file skeleton is found in [qeflow.cfg](examples/qeflow.cfg). In the following we show 2 examples.

1. **Local** configuration: useful we running simulation on a personal computer.

    ```yaml
    # $HOME/.qeflow.cfg
    cluster: local
    pwx: path/to/pw.x
    mpix: path/to/mpirun
    ```

2. **Slurm** configuration: this is necessary when we are logged in a HPC facility with a [slurm] batch system.

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

In the future, I might implement also the [PBS] batch system.

### 2. Input file

The input file skeleton with the currently supported flags and relative description is found in [qeflow.in](examples/qeflow.in).
In the following I'll show only 3 minimal examples:

1. a simple `scf` calculation with different values of `ecutwfc`;
2. a `scf` followed by `nscf` with respect to both `ecutwfc` and `kpoints`
3. a `vc-relax` followed by a `nscf` at the relaxed structure.

#### 2.1 Convergence of `scf` workflow

We want to perform a simple `scf` calculation with different values of `ecutwfc`. The input file is a [yaml] file, name it `ecutSi.in` (can be any name, actually) and type the following:

```yaml
# ecutSi.in
---
name: ecutSi
workflow:
    - scf:
withrespectto:
    - ecutwfc: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

nprocs: 128
time: 0:20:0
partition: standard
qos: short

pseudo_pots    : [Si.pbe-n-rrkjus_psl.1.0.0.UPF]
atoms          : [Si]
masses         : [28.085]
positions      : [[ Si,    0.0,    0.0,     0.0 ],
                  [ Si, 1.3575, 1.3575,  1.3575 ]]
unit_cell      : [[ 2.715, 2.715,   0.0 ],
                  [   0.0, 2.715, 2.715 ],
                  [ 2.715,   0.0, 2.715 ]]

kpoints        : [8, 8, 8]
prefix         : silicon
pseudo_dir     : /path/to/SSSP_efficiency
```

The first three flags are the workflow instructions:

- `name`: a unique name to identify this workflow, a folder with the same name will be created, containing the results of the calculations;
- `workflow`: a list of **tasks**. In this case we only have one task, the scf calcualtion;
- `withrespectto`: a list of **parameters**, where each of them is a also a list. In this case we only have one parameter `ecutwfc` spanning values from 10 to 100 Ry.

The second block of instruction applies only when running on a HPC. In this case we have the usual [slurm] specifications for number of processors, allocation time, partition and quality of service.

Finally, the third block of flags contains all the usual [quantum espresso keys](https://www.quantum-espresso.org/Doc/INPUT_PW.html) necessary for this calculation. The order in which they appear does not matter, just dump them in there (also remember to look at the definitions in [qeflow.in](examples/qeflow.in)).

Now it's time to run the workflow: the executable to call is simply `qeflow`. You can type `qeflow -h` for a short help menu showing other options such as `dry-run` and `verbosity`. Now type:

```bash
qeflow ecutSi.in
```

And that's it! After the calculation is done you should have all your calculations and results collected into a folder named `ecutSi`.

Most importantly, QE-flow parses automatically the most important properties of the system and collects them into a file in the results folder: `./ecutSi/results/silicon.txt`. You can inspect this file using [yaml] and [pandas]:

```python
import yaml
import pandas
with open('./ecutSi/results/silicon.txt', 'r') as f:
    data = yaml.safe_load(f)
df = pandas.DataFrame(data)
print(df[['ecutwfc','etot']])
```

The output is the following:

```x
   ecutwfc        etot
0       10 -310.790657
1       20 -310.720741
2       30 -310.744642
3       40 -310.746610
4       50 -310.747418
5       60 -310.747733
6       70 -310.747919
7       80 -310.748074
8       90 -310.748119
9      100 -310.748170
```

#### 2.2 A `scf` followed by `nscf` workflow, as function of `ecutwfc` and `kpoint`

In this example we show a more complex workflow, where we converge a calculation with respect to 2 parameters. The workflow instructions are the following

```yaml
# ecutKpointSi.in
---
name: ecutKpointSi
workflow:
    - scf:
    - nscf:
        kpoints: [12,12,12]
withrespectto:
    - ecutwfc: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    - kpoints: [[4,4,4], [8,8,8], [12,12,12]]

# below this point is the same as in the previous example
```

The are some differences compared to the previous case:

- the workflow flag is now a list of 2 **tasks**: `scf` and `nscf`;
- the second `nscf` task declares `kpoints: [12,12,12]`: this overwrites any other kpoint declaration defined later in the input file;
- the withrespectto flag also has 2 entries: the final workflow will be the **cartesian product** of `ecutwfc` and `kpoints` values.

This means that the `scf + nscf` workflow will be performed 30 times, each time with a different `ecutwfc` and `kpoints`, but keeping the `nscf` kpoints fixed.

Everythong else remains the same. Data are collected in `./ecutKpointSi/results/silicon.txt` and can be inspected with [yaml] and [pandas].

#### 2.3 A `vc-relax` followed by `nscf` workflow

Finally, last example is a `vc-relax` plus a `nscf` at the relaxed structure with no iterations to check convergence. The workflow instructions are

```yaml
# relaxSi.in
---
name: relaxSi
workflow:
    - vc-relax:
        ecutwfc: 80
        mixing_beta: 0.6
    - nscf:
        kpoints: [12,12,12]
        mixing_beta: 0.7

# below this point is the same as the first case
```

The `withrespectto` flag is missing. No variation over any parameter will be performed. However, we can always fine tune each task by defining a specific flag that overwrites the default ones (given in the bottom section, not shown).

That's all for now.

## Support

For any problems, questions or suggestions, please contact me at `tenobaldi@gmail.com`.

## Roadmap

Currently this is a very basic python script. But I'll try to keep working on it, as long as I keep doing science, which is definitely not guaranteed LOL!  
Anyway, future developments will include:

- `pp.x`, `dos.x`, `bands.x`, `projwfc.x`, `plotband.x`, `wannier90.x`, `pw2w90.x` support;
- more QE flags, with priority to:
  - ibrav different from 0;
  - kpoints for BZ path and band structure;
- more parsing options;
- intelligent parsing for dependent calculations.

## Authors and acknowledgment

The development of QE-flow is proudly powered by [me](https://github.com/t3n0).  
[Quantum Espresso](https://www.quantum-espresso.org/manifesto/) is licensed under GPL3 and citation guidelines can be found [here](https://www.quantum-espresso.org/Doc/user_guide/node6.html#SubSec:Terms) and [here](https://www.quantum-espresso.org/Doc/user_guide/node3.html).

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

[pandas]: https://pandas.pydata.org/
[yaml]: https://yaml.org/
[pbs]: https://en.wikipedia.org/wiki/Portable_Batch_System
[slurm]: https://slurm.schedmd.com/overview.html
