
from qeflow.logger import Logger
from math import ceil

class Slurm(object):
    def __init__(self, inp, cfg, logger = Logger()) -> None:
        self.logger = logger
        self.inp = inp
        self.cfg = cfg

    def save(self):
        cfgDict = self.cfg.configs
        inpDict = self.inp.inp
        tasks = self.inp.getTasks()
        # define nodes and task_per_node
        self.logger.info(f'Initialising Slurm script.', 1)
        cores_per_node = cfgDict['cores_per_node']
        nprocs = inpDict['nprocs']
        nodes = ceil(nprocs / cores_per_node)
        task_per_node = nprocs // nodes
        nprocs_new = nodes*task_per_node
        self.logger.info(f' * reqeusted {nprocs} cpus, with {cores_per_node} cores per node.', 2)
        self.logger.info(f' * the job will be run over {nodes} nodes', 2)
        self.logger.info(f' * with {task_per_node} mpi processes per node', 2)
        self.logger.info(f' * using a total of {nprocs_new} cpus', 2)

        # plug the above into the input dictionary
        slurmInp = {
            'job_name' : inpDict['name'].split('/')[-1],
            'nodes' : nodes,
            'task_per_node' : task_per_node,
            'cpu_per_task' : 1,
            'time' : inpDict['time'],
            'account' : cfgDict['account'],
            'partition' : inpDict['partition'],
            'qos' : inpDict['qos'],
        }

        # define the python environment
        if 'pyenv' in cfgDict.keys():
            slurmInp['pyenvBlock'] = f'source {cfgDict['pyenv']}'
        else:
            slurmInp['pyenvBlock'] = ''
        
        # define modules to load
        if 'modules' in cfgDict.keys():
            text = ''
            for m in cfgDict['modules']:
                text += f'module load {m}\n'
            slurmInp['modulesBlock'] = text
        else:
            slurmInp['modulesBlock'] = ''

        # append tasks to slurm file
        text = ''
        inputPath = self.inp.path
        for i, task in enumerate(tasks):
            text += f'srun --nodes=1 --ntasks=1 --ntasks-per-node=1 --exact --mem=1500M qeflow {inputPath} -i {i}\n'
            if task['task'] in pwTasks:
                text += f'srun --distribution=block:block --hint=nomultithread {cfgDict['pwx']} -in {task['fileNameIn']} >> {task['fileNameOut']}\n'
            if task['task'] in dosTasks:
                text += f'srun --distribution=block:block --hint=nomultithread {cfgDict['dosx']} -in {task['fileNameIn']} >> {task['fileNameOut']}\n'
            if task['task'] in phTasks:
                text += f'srun --distribution=block:block --hint=nomultithread {cfgDict['phx']} -in {task['fileNameIn']} >> {task['fileNameOut']}\n'
            if task['task'] in w90Tasks:
                text += f'srun --distribution=block:block --hint=nomultithread {cfgDict['w90x']} {task['fileNameIn']} >> {task['fileNameOut']}\n'
            if task['task'] in w90ppTasks:
                text += f'srun --distribution=block:block --hint=nomultithread {cfgDict['w90x']} -pp {task['fileNameIn']} >> {task['fileNameOut']}\n'
            if task['task'] in pw2w90Tasks:
                text += f'srun --distribution=block:block --hint=nomultithread {cfgDict['pw2w90x']} {task['fileNameIn']} >> {task['fileNameOut']}\n'
        # print(text)

        slurmInp['srunBlock'] = text
        print()
        print(slurmSkel.format(**slurmInp))

    def run(self):
        pass


pwTasks = [
    'scf',
    'nscf',
    'bands',
    'relax',
    'vc-relax',
    'md',
    'vc-md',
]

dosTasks = [
    'dos',
]

phTasks = [
    'ph',
]

w90Tasks = [
    'w90',
]

w90ppTasks = [
    'w90pp',
]

pw2w90Tasks = [
    'pw2w90',
]

slurmSkel = '''
#!/bin/bash --login

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