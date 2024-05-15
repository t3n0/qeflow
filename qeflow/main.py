'''
qeflow main file for entry scripts
'''


from qeflow import __version__
from qeflow.parsers import getArgsQeflow, getArgsQeparse, getArgsQetask
from qeflow.utils import removeFile, runProcess
from qeflow.logger import Logger
from qeflow.config import readConfig
from qeflow.inputs import readInput, readYaml
from qeflow.workflow import createWorkflow
from qeflow.slurm import createSlurm
from qeflow.tasks import createTask, runTask, parseTask
from datetime import datetime


def qeflow():
    try:
        removeFile('./crash.txt')
        args = getArgsQeflow()
        DRY = args.dry
        INPUTPATH = args.inputFile
        VERBOSE = args.verbose

        logger = Logger(VERBOSE)
        logger.info(f'\n-------- Welcome to QE-flow, version {__version__} --------', 1)
        logger.info(f'\nThis run has started on {datetime.now().strftime("%d %b %Y, %H:%M:%S")}.', 1)

        if DRY:
            logger.info(f'\n--------------------------------', 1)
            logger.info(f'This is a dry run.', 1)
            logger.info(f'No calculations will be performed:', 1)
            logger.info(f' * all inputs are checked;', 1)
            logger.info(f' * workflow and logger are printed to file.', 1)

        # read input and config
        config = readConfig(logger)
        input = readInput(INPUTPATH, logger)
        # create workflow and save it to file
        workflowList = createWorkflow(input, config, logger)

        cluster = config['cluster']
        if cluster == 'slurm': slurmPath = createSlurm(input, config, workflowList, logger)

        if DRY:
            logger.info(f'\n--------------------------------', 1)
            logger.info(f'Dry run done.', 1)
            logger.saveLog(input['logger_path'], 'w')
        else:
            if cluster == 'slurm':
                logger.info(f'\n--------------------------------', 1)
                logger.info(f'Running using slurm system.', 1)
                runProcess('sbatch', slurmPath)
                logger.info(f'\n--------------------------------', 1)
                logger.info(f'Slurm script submitted succesfully.', 1)
                logger.saveLog(input['logger_path'], 'w')

            elif cluster == 'local':
                logger.info(f'\n--------------------------------', 1)
                logger.info(f'Running on the local environment using {input["nprocs"]} processors.\n', 1)
                for i, workflow in enumerate(workflowList):
                    logger.info(f'Running workflow {i}: {workflow[0]["domain"]}', 1)
                    for j, task in enumerate(workflow):
                        logger.info(f' * task {j}: {task["task"]}', 1)
                        createTask(task, logger)
                        runTask(task, logger)
                        parseTask(task, logger)
                logger.info(f'\n--------------------------------', 1)
                logger.info('All workflows performed succesfully.', 1)
                logger.saveLog(input['logger_path'], 'w')
            else:
                logger.info(f' * Error: cluster = {cluster} not recognised')
                raise Exception('WrongKeyError')
    except Exception as error:
        logger.info(f'Error: {error}')
        logger.saveLog('./crash.txt', 'w')
        exit(1)


def qetask():
    try:
        args = getArgsQetask()
        logger = Logger()
        INPUTPATH = args.workflowFile
        I = args.i
        J = args.j
        workflowList = readYaml(INPUTPATH)
        task = workflowList[I][J]
        logger.info(f'Creating inputfile: work-task {I:03d}-{J:03d}')
        createTask(task, logger)
        logger.saveLog(task['logger_path'], 'a')
    except Exception as error:
        logger.info(f'Error: {error}')
        logger.saveLog('./crash.txt', 'w')
        exit(1)


def qeparse():
    try:
        args = getArgsQeparse()
        logger = Logger()
        INPUTPATH = args.workflowFile
        I = args.i
        J = args.j
        workflowList = readYaml(INPUTPATH)
        task = workflowList[I][J]
        logger.info(f'Parsing inputfile: work-task {I:03d}-{J:03d}')
        parseTask(task, logger)
        logger.saveLog(task['logger_path'], 'a')
    except Exception as error:
        logger.info(f'Error: {error}')
        logger.saveLog('./crash.txt', 'w')
        exit(1)