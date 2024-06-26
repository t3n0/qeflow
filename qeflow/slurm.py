
from qeflow.logger import Logger
from math import ceil
import os


def createSlurm(inp, cfg, wfList, logger = Logger()):
    # define nodes and task_per_node
    logger.info(f'\n--------------------------------', 1)
    logger.info(f'Initialising Slurm script.', 1)
    cores_per_node = cfg['cores_per_node']
    nprocs = inp['nprocs']
    nodes = ceil(nprocs / cores_per_node)
    task_per_node = nprocs // nodes
    nprocs_new = nodes*task_per_node
    logger.info(f' * reqeusted {nprocs} cpus, with {cores_per_node} cores per node.', 2)
    logger.info(f' * the job will be run over {nodes} nodes', 2)
    logger.info(f' * with {task_per_node} mpi processes per node', 2)
    logger.info(f' * using a total of {nprocs_new} cpus', 2)
    slurmInp = {
        'job_name' : inp['name'].split('/')[-1],
        'nodes' : nodes,
        'task_per_node' : task_per_node,
        'cpu_per_task' : 1,
        'time' : inp['time'],
        'account' : cfg['account'],
        'partition' : inp['partition'],
        'qos' : inp['qos'],
        }
    # define the python environment
    if 'pyenv' in cfg.keys():
        logger.info(f'Loading python environment from:\n   {cfg["pyenv"]}', 1)
        slurmInp['pyenvBlock'] = f'source {cfg["pyenv"]}'
    else:
        slurmInp['pyenvBlock'] = ''
    
    # define modules to load
    if 'modules' in cfg.keys():
        logger.info(f'Loading modules.', 1)
        text = ''
        for m in cfg['modules']:
            logger.info(f' * module load {m}', 2)
            text += f'module load {m}\n'
        slurmInp['modulesBlock'] = text
    else:
        slurmInp['modulesBlock'] = ''

    # append tasks to slurm file
    text = ''
    workflowPath = inp['workflow_path']
    logger.info(f'Appending tasks to slurm batch file.', 1)
    for i, work in enumerate(wfList):
        for j, task in enumerate(work):
            text += f'srun --nodes=1 --ntasks=1 --ntasks-per-node=1 --exact --mem=1500M qetask {workflowPath} -i {i} -j {j}\n'
            text += f'srun {cfg[task["task"]]} -in {task["fileNameIn"]} >> {task["fileNameOut"]}\n'
            text += f'srun --nodes=1 --ntasks=1 --ntasks-per-node=1 --exact --mem=1500M qeparse {workflowPath} -i {i} -j {j}\n'

    slurmInp['srunBlock'] = text
    
    slurmPath = os.path.join(inp['calc_dir'], 'slurm.sub')
    os.makedirs(os.path.dirname(slurmPath), exist_ok=True) # creates the necessary folders
    logger.info(f'Saving slurm batch file to disk:\n   {slurmPath}', 1)
    with open(slurmPath, 'w') as slurmfile:
        slurmfile.write(slurmSkel.format(**slurmInp))
    
    return slurmPath


slurmSkel = '''#!/bin/bash --login

#SBATCH --job-name={job_name}
#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={task_per_node}
#SBATCH --cpus-per-task={cpu_per_task}
#SBATCH --time={time}
#SBATCH --distribution=block:block
#SBATCH --hint=nomultithread

#SBATCH --account={account}
#SBATCH --partition={partition}
#SBATCH --qos={qos}

{pyenvBlock}

{modulesBlock}

export OMP_NUM_THREADS=1
export SRUN_CPUS_PER_TASK=${{SLURM_CPUS_PER_TASK}}

{srunBlock}
'''