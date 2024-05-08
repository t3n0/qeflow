import itertools
from qeflow.utils import saveYaml
from qeflow.logger import Logger
import os


def createWorkflow(inp, logger = Logger()):
    '''
    Returns a list of dictionaries. Each dictionary is the input of a specific code in the workflow.
    Also, each dictionary is the cartesian product of the `withrespectto` flag entries.
    '''

    # this will be dump in the workflow json
    # it is the list of all workflows ordered by the domain entry
    workflowList = []

    # some logging
    logger.info(f'\n--------------------------------', 1)
    logger.info(f'Workflow that will be performed:', 1)
    for task in inp['tasks']:
        logger.info(f' * {task}', 1)
    
    # define the domain of the wrt parameters
    # if the wrt flag is not given the domain is a list with only one element, an empty dictionary
    # domainDictList = [ {} ]
    paramNames, paramValues = listProduct(inp['withrespectto'])
    domainDictList = dictProduct(paramNames, paramValues)

    # some logging
    logger.info(f'Each workflow will iterate {len(domainDictList)} times.', 1)
    logger.info(f'Iterating parameters:', 1)
    for wrt in domainDictList:
        logger.info(f' * { wrt }', 1)

    # if overwrite is true, all workflows will be performed in the same folder
    # also, if there is no wrt flag (i.e. we only perform one workflow)
    # all tasks will be performed in the same folder
    for i, domain in enumerate(domainDictList):
        workflow_this_domain = {}        
        # define the tasks
        workflow_this_domain['tasks'] = []
        for j, (work, task) in enumerate(zip(inp['workflow'], inp['tasks'])):
            # we dump all the key-values from the main input file
            aux = (inp | work[task]) | domain
            aux = removeKeys(aux, keysToRemove)
            # adding some new flags
            aux['task'] = task
            if inp['overwrite'] == True or len(domainDictList) == 1:
                aux['work_dir'] = inp['calc_dir']
            else:
                aux['work_dir'] = os.path.join(inp['calc_dir'], f'w{i:03d}')
            aux['fileNameIn'] = os.path.join(aux['work_dir'], f'{j:02d}.{task}.in')
            aux['fileNameOut'] = os.path.join(aux['work_dir'], f'{j:02d}.{task}.out')
            workflow_this_domain['tasks'].append(aux)
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
    'overwrite',
]


