'''
qeflow main file for entry scripts
'''


from qeflow.parsers import getArgs


def main():
    '''
    Main qeflow executable.
    Reads the mandatory input file and setup the workflow.
    If running locally, the workflow is executed from within pyhton.
    If running on an HPC, a Slurm script is generated, launched and the code exits.
    '''
    
    args = getArgs()

    print(args)
