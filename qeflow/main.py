'''
qeflow main file for entry scripts
'''


from qeflow.parsers import getArgs


def main():
    print('hello from qeflow main script')
    args = getArgs()

    print(args)
