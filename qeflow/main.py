'''
qeflow main file for entry scripts
'''


from qeflow import __version__
from qeflow.parsers import getArgs
from qeflow.logger import Logger
from qeflow.config import readConfig
from qeflow.inputs import readInput
from qeflow.workflow import createWorkflow
from qeflow.utils import createDir, runProcess, removeFile, readYaml, runTask, appendResults
from qeflow.slurm import createSlurm


def main():
    '''
    Main qeflow executable.
    Reads the mandatory input file and setup the workflow.
    If running locally, the workflow is executed from within pyhton.
    If running on an HPC, a Slurm script is generated, launched and the code exits.
    '''
    
    args = getArgs()
    DRY = args.dry
    INPUTPATH = args.inputFile
    VERBOSE = args.verbose

    logger = Logger(VERBOSE)
    if DRY:
        logger.info(f'This is a dry run.', 1)
        logger.info(f'No calculations will be performed:', 1)
        logger.info(f' * the folder structure is created;', 1)
        logger.info(f' * all inputs are checked;', 1)
        logger.info(f' * workflow and logger are printed to file.', 1)


    # read input and config
    config = readConfig(logger)
    input = readInput(INPUTPATH, logger)

    # create folders
    logger.info(f'\n--------------------------------', 1)
    createDir(input['name'], logger)
    createDir(input['calc_dir'], logger)
    createDir(input['res_dir'], logger)

    # create workflow
    workflow = createWorkflow(input, logger)

    cluster = config['cluster']
    if cluster == 'slurm': slurmPath = createSlurm(input, config, workflow, logger)

    if DRY:
        logger.info(f'\n--------------------------------', 1)
        logger.info(f'Dry run done.', 1)
        logger.saveLog(input['logger_path'], 'w')
    else:
        if cluster == 'slurm':
            print('run slurm')
            #runProcess('sbatch', slurmPath)
        elif cluster == 'local':
            print('run local')
            for task in workflow:
                runTask(task)
                appendResults(task)
        else:
            logger.info(f' * Error: cluster = {cluster} not recognised')
            raise Exception('WrongKeyError')
