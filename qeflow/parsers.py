'''
Module with all the parsers
'''

from qeflow import __version__
from qeflow.constants import *
import argparse
import xmltodict

def getArgs():
    parser = argparse.ArgumentParser(
        prog = 'qeflow',
        description='QE-flow: automating quantum espresso workflows without scassamento di maroni.')
    parser.add_argument("inputFile", help="input file, mandatory", type=str)
    parser.add_argument("-d", "--dry", help="dry run: parse input, setup workflow and exit. No code is run.", action='store_true')
    parser.add_argument("-v", "--verbose", help="verbosity level counter, e.g. -vvv = 3", action='count', default=0)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument("-i", "--iter", help=argparse.SUPPRESS, type=int) # option hidden to the user, maybe I'll implement this later
    return parser.parse_args()


def parseAtomicPositions(path):
    '''
    Parse the xml file output by QE
    '''
    with open(path, 'r') as f:
        data = xmltodict.parse(f.read())
    atoms = data['qes:espresso']['output']['atomic_structure']['atomic_positions']['atom']
    positions = []
    for atom in atoms:
        x,y,z = atom['#text'].split()
        pos = [atom['@name'],
               float(x)*B2A,
               float(y)*B2A,
               float(z)*B2A]
        positions.append(pos)
    return positions


def parseUnitCell(path):
    '''
    Parse the xml file output by QE
    '''
    with open(path, 'r') as f:
        data = xmltodict.parse(f.read())
    cell = data['qes:espresso']['output']['atomic_structure']['cell']
    unitCell = []
    for k in ['a1', 'a2', 'a3']:
        x,y,z = cell[k].split()
        unitCell.append([float(x)*B2A, float(y)*B2A, float(z)*B2A])
    return unitCell


def parseFermiEnergy(path):
    with open(path, 'r') as f:
        data = xmltodict.parse(f.read())
    fermi_energy = data['qes:espresso']['output']['band_structure']['fermi_energy']
    return float(fermi_energy)*H2E


def parseTotalEnergy(path):
    with open(path, 'r') as f:
        data = xmltodict.parse(f.read())
    energies = data['qes:espresso']['output']['total_energy']
    total = 0
    for k,v in energies.items():
        total += float(v)
    return float(energies['etot'])*H2E