import itertools
from qeflow.utils import saveYaml
from qeflow.logger import Logger
import os


def createWorkflow(inp, logger = Logger()):
    '''
    Returns a list of lists:
        workflowList = [
            workflow1,
            workflow2,
            etc,
        ]
    Where each workflow is a list of tasks, for a given `wrt` flag:
        workflow1 = [scf, nscf, dos], with ecutwfc = 40
        workflow2 = [scf, nscf, dos], with ecutwfc = 60
        etc
    '''

    workflowList = []

    logger.info(f'\n--------------------------------', 1)
    logger.info(f'Workflow that will be performed:', 1)
    for task in inp['tasks']:
        logger.info(f' * {task}', 1)
    
    # define the domain of the wrt parameters
    # if the wrt flag is not given, domainDictList = [ {} ]
    paramNames, paramValues = listProduct(inp['withrespectto'])
    domainDictList = dictProduct(paramNames, paramValues)

    logger.info(f'Each workflow will iterate {len(domainDictList)} times.', 1)
    logger.info(f'Iterating parameters:', 1)
    for wrt in domainDictList:
        logger.info(f' * { wrt }', 1)

    for i, domain in enumerate(domainDictList):
        workflow_this_domain = []
        for j, (work, task) in enumerate(zip(inp['workflow'], inp['tasks'])):
            # we dump all the key-values from the main input file
            thisTask = (inp | work[task]) | domain
            thisTask = removeKeys(thisTask, keysToRemove)
            # adding some new flags
            thisTask['task'] = task
            thisTask['work_dir'] = os.path.join(inp['calc_dir'], f'w{i:03d}')
            thisTask['fileNameIn'] = os.path.join(thisTask['work_dir'], f'{j:02d}.{task}.in')
            thisTask['fileNameOut'] = os.path.join(thisTask['work_dir'], f'{j:02d}.{task}.out')
            workflow_this_domain.append(thisTask)
        workflowList.append(workflow_this_domain)
    
    # some logginh and saving to disk
    logger.info(f'Save workflow file to disk:\n   {inp['workflow_path']}', 1)
    saveYaml(workflowList, inp['workflow_path'])

    # # data is the dictionary of the results
    # # we start by filling it with the domain parameters
    # # e.g. data['ecutwfc'] = [20, 20, 40, 40]
    # # e.g. data['ecutrho'] = [200, 400, 200, 400]
    # data = {}
    # for i, par in enumerate(params):
    #     data[par] = [product[j][i] for j in range(len(product))]

    return workflowList


def listProduct(dictList):
    params = []
    valuesList = []
    for wrt in dictList:
        for k, v in wrt.items():
            params.append(k)
            valuesList.append(v)
    return params, list(itertools.product(*valuesList))


def dictProduct(keys, listValues):
    wrtDicts = []
    for values in listValues:
        aux = {}
        for k,v in zip(keys, values):
            aux[k] = v
        wrtDicts.append(aux)
    return wrtDicts


def removeKeys(d, listKeys):
    for k in listKeys:
        del d[k]
    return d


keysToRemove = [
    'workflow',
    'workflow_path',
    'calc_dir',
    'tasks',
    'withrespectto',
    'nprocs',
    'time',
    'partition',
    'qos',
]


