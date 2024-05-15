# QE-flow changelog

All notable changes of [qeflow](qeflow) releases.  
For the development unreleased (and unstable) version see [here](unreleased).

## [QE-flow v0.1](https://github.com/t3n0/qeflow/releases/tag/v0.1) (2024-05-15)

### Added

- Basic setup files (README.md, LICENSE, CHANGELOG.md, pyproject.toml)
- Simple logging features:
  - output log.txt
- Input file in [yaml] format
  - workflow flag as a list of tasks
  - iterations as a list of keywords
- Automatic parsing and collection of the results in an output database file. Data currently parsed:
  - fermi, total, ewald, eband, ehart, etxc, vtxc energies
- Possibility to perform a dry run:
  - no calculations are executed
  - creation of folder structure, workflows and database skeleton
- Basic input file checks and error handling
- Very simple support for [slurm](slurm) HPC submission systems
  - job_name, nodes, task_per_node, cpu_per_task, time, account, partition, qos, module loads, source environments
- Possibility to run the workflow on a local machine as well
- Quantum epresso support for pw.x code. Only the following keys are currently implemented
  - CONTROL:
    - calculation: scf, nscf, vc-relax.
  - SYSTEM
    - ibrav = 0
    - prefix, pseudo_dir, outdir, verbosity, nat, ntyp, ecutwfc, lspinorb, noncolin, nosym, assume_isolated
  - ELECTRONS
    - conv_thr, mixing_beta
  - ATOMIC_SPECIES
  - CELL_PARAMETERS angstrom
  - ATOMIC_POSITIONS angstrom
  - IONS
  - CELL
    - cell_dofree: all, 2Dxy
  - K_POINTS automatic, crystal

[yaml]: https://yaml.org/
[slurm]: https://slurm.schedmd.com/overview.html
[qeflow]: https://github.com/t3n0/qeflow
[unreleased]: https://github.com/t3n0/qeflow/tree/develop
