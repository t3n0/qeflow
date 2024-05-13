'''
Functions for the pw.x executable
'''

from qeflow.constants import *
from qeflow.parsers import parseTotalEnergy, parseFermiEnergy
from qeflow.utils import readYaml, saveYaml


def createPwx(inp: dict):
    '''
    Creates a pw.x input file based on the `inp` dictionary
    '''
    userInp = {
        'calc' : inp['task'],
        'outdir' : os.path.join(inp['calc_work_dir'], 'outdir'),
        'pseudo_dir' : os.path.abspath(os.path.join(CWD, inp['pseudo_dir'])),
        'nat' : len(inp['positions']),
        'ntyp' : len(inp['atoms']),}
    inp = defaultKeys | inp
    userInp['atomicSpeciesBlock'] = atomicSpeciesBlock(inp)
    userInp['atomicPositionsBlock'] = atomicPositionsBlock(inp)
    userInp['kPointsBlock'] = kPointsBlock(inp, inp['kpoints_mode'])
    userInp['cellParametersBlock'] = unitCellBlock(inp)
    userInp['ionsBlock'] = ionsBlock(inp)
    userInp['cellBlock'] = cellBlock(inp)

    text = pwxSkel.format(**(inp | userInp))
    os.makedirs(os.path.dirname(inp['fileNameIn']), exist_ok=True) # creates the necessary folders
    with open(inp['fileNameIn'], 'w') as f: 
        f.write(text)


def parsePwx(inp: dict):
    old_xml_path = os.path.join(inp['calc_work_dir'], 'outdir', f'{inp['prefix']}.xml')
    new_xml_path = os.path.join(inp['res_work_dir'], f'{inp['task_indices'][1]:02d}.{inp['task']}.xml')
    os.makedirs(os.path.dirname(new_xml_path), exist_ok=True) # creates the necessary folders
    os.rename(old_xml_path, new_xml_path)
    data = readYaml(inp['dataFile'])
    if inp['task'] == 'scf':
        totalE = parseTotalEnergy(new_xml_path)
        if 'totalE' in data.keys():
            data['totalE'].append(totalE)
        else:
            data['totalE'] = [totalE]
    elif inp['task'] == 'nscf':
        fermiE = parseFermiEnergy(new_xml_path)
        if 'fermiE' in data.keys():
            data['fermiE'].append(fermiE)
        else:
            data['fermiE'] = [fermiE]
    saveYaml(data, inp['dataFile'])
    

def unitCellBlock(inp):
    # only when ibrav = 0
    # right now this is always the case
    text = 'CELL_PARAMETERS angstrom\n'
    text += '  {unit_cell[0][0]} {unit_cell[0][1]} {unit_cell[0][2]}\n'.format(**inp)
    text += '  {unit_cell[1][0]} {unit_cell[1][1]} {unit_cell[1][2]}\n'.format(**inp)
    text += '  {unit_cell[2][0]} {unit_cell[2][1]} {unit_cell[2][2]}\n'.format(**inp)
    return text


def atomicSpeciesBlock(inp):
    # this is correct
    text = 'ATOMIC_SPECIES\n'
    for atom, mass, pot in zip(inp['atoms'], inp['masses'], inp['pseudo_pots']):
        text += f'  {atom} {mass} {pot}\n'
    return text


def atomicPositionsBlock(inp):
    # no implemented flags: if_pos(1), if_pos(2), if_pos(3)
    # maybe in the future
    pos = inp['positions']
    if pos == 'vc-relax':
        print('helloooooooooooooooooooooo')
    else:
        text = 'ATOMIC_POSITIONS angstrom\n'
        for p in pos:
            text += f'  {p[0]} {p[1]} {p[2]} {p[3]}\n'
    return text


def ionsBlock(inp):
    # possible flags are:
    # ion_positions, ion_velocities, ion_dynamics, pot_extrapolation, wfc_extrapolation, remove_rigid_rot
    # ion_temperature, tempw, tolp, delta_t, nraise, refold_pos, upscale, bfgs_ndim, trust_radius_max
    # trust_radius_min, trust_radius_ini, w_1, w_2, fire_alpha_init, fire_falpha, fire_nmin, fire_f_inc, fire_f_dec, fire_dtmax
    # none of them is currently implemented
    if inp['task'] in ['relax', 'md', 'vc-relax', 'vc-md']:
        text = '&IONS\n'
        text += '/'
    else:
        text = ''
    return text


def cellBlock(inp):
    # possible flags are: cell_dynamics, press, wmass, cell_factor, press_conv_thr, cell_dofree
    # right now only ceel-dofree is implemented
    if inp['task'] in ['vc-relax', 'vc-md']:
        text = '&CELL\n'
        text += f'  cell_dofree = {inp['cell_dofree']}\n'
        text += '/'
    else:
        text = ''
    return text


def kPointsBlock(inp, mode):
    # mode can be: tpiba | automatic | crystal | gamma | tpiba_b | crystal_b | tpiba_c | crystal_c
    # right now only automatic and crystal are implemented
    if mode == 'automatic':
        kpoints = inp['kpoints']
        offset = inp['kpoints_offset']
        text = 'K_POINTS automatic\n'
        text += f'  {kpoints[0]} {kpoints[1]} {kpoints[2]} {offset[0]} {offset[1]} {offset[2]}\n'
    elif mode == 'crystal':
        kpoints = inp['kpoints']
        nk1, nk2, nk3 = kpoints[0], kpoints[1], kpoints[2]
        w = 1/nk1/nk2/nk3
        text = 'K_POINTS crystal\n'
        text += f'  {nk1*nk2*nk3}\n'
        for k1 in range(nk1):
            for k2 in range(nk2):
                for k3 in range(nk3):
                    text += f'{k1/nk1:12.8f} {k2/nk2:12.8f} {k3/nk3:12.8f} {w:14.6e}\n'
    return text

# def kPointsBlock(inp, mode):
#     if mode == 'scf':
#         kpoints = inp['scf_kpoints']
#         text = 'K_POINTS automatic\n'
#         text += f'  {kpoints[0]} {kpoints[1]} {kpoints[2]} 0 0 0\n'
#     elif mode == 'nscf':
#         kpoints = inp['nscf_kpoints']
#         nk1, nk2, nk3 = kpoints[0], kpoints[1], kpoints[2]
#         w = 1/nk1/nk2/nk3
#         text = 'K_POINTS crystal\n'
#         text += f'  {nk1*nk2*nk3}\n'
#         for k1 in range(nk1):
#             for k2 in range(nk2):
#                 for k3 in range(nk3):
#                     text += f'{k1/nk1:12.8f} {k2/nk2:12.8f} {k3/nk3:12.8f} {w:14.6e}\n'
#     elif mode == 'w90':
#         kpoints = inp['nscf_kpoints']
#         nk1, nk2, nk3 = kpoints[0], kpoints[1], kpoints[2]
#         text = 'beggin kpoints\n'
#         for k1 in range(nk1):
#             for k2 in range(nk2):
#                 for k3 in range(nk3):
#                     text += f'{k1/nk1:12.8f} {k2/nk2:12.8f} {k3/nk3:12.8f}\n'
#         text += 'end kpoints\n'
#     return text



pwxSkel = '''
&CONTROL
  calculation  = "{calc}"
  prefix       = "{prefix}"
  pseudo_dir   = "{pseudo_dir}"
  outdir       = "{outdir}"
  verbosity    = "{verbosity}"
/

&SYSTEM
  ibrav        = 0
  nat          = {nat}
  ntyp         = {ntyp}
  ecutwfc      = {ecutwfc}
  lspinorb     = {lspinorb}
  noncolin     = {noncolin}
  nosym        = {nosym}
  assume_isolated = "{assume_isolated}"
/

&ELECTRONS
  conv_thr    = {conv_thr}
  mixing_beta = {mixing_beta}
/

{atomicSpeciesBlock}
{atomicPositionsBlock}
{kPointsBlock}
{cellParametersBlock}
{ionsBlock}
{cellBlock}
'''


defaultKeys = {
    'prefix' : 'mycalc',
    'pseudo_dir' : os.path.join(HOME, 'ppdir'),
    'verbosity' : 'low',
    'ecutwfc' : 50,
    'lspinorb' : False,
    'noncolin' : False,
    'nosym' : False,
    'assume_isolated' : 'none',
    'conv_thr' : 1e-8,
    'mixing_beta' : 0.7,
    'kpoints_mode' : 'automatic',
    'kpoints_offset' : [0, 0, 0],
    'cell_dofree' : 'all'}
