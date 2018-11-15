from __future__ import print_function
import argparse
import csv
from collections import OrderedDict
from copy import deepcopy

CONSTANTES_FILE = 'constants.csv'
CALENDARIO_FILE = 'Calendario.csv'

with open(CONSTANTES_FILE) as f:
    CONSTANTES = list(csv.DictReader(f))

with open(CALENDARIO_FILE) as f:
    EVENTOS_RAW = list(csv.DictReader(f))

PERIODISTAS = ['P1', 'P2', 'P3', 'P4', 'P5']
CANALES = ['C1', 'C2']
DIAS = ['D{}'.format(n) for n in range(1, 12+1)]
CATEGORIAS = ['A', 'B', 'C', 'D', 'E']
DEPORTES = [x['deporte'] for x in CONSTANTES] # Mismo orden que el archivo
DEPORTES_SHORT = {
    'arqueria': 'ARQ',
    'atletismo': 'ATL',
    'badminton': 'BAD',
    'baile': 'BAI',
    'basquet': 'BAS',
    'handball': 'HAN',
    'boxeo': 'BOX',
    'ciclismo': 'CIC',
    'equitacion': 'EQU',
    'escalada': 'ESC',
    'esgrima': 'ESG',
    'futsal': 'FUT',
    'gimnasia': 'GIM',
    'golf': 'GOL',
    'halterofilia': 'HAL',
    'hockey': 'HOC',
    'judo': 'JUD',
    'karate': 'KAR',
    'lucha': 'LUC',
    'natacion': 'NAT',
    'pentatlon': 'PEN',
    'remo': 'REM',
    'rugby': 'RUG',
    'taekwondo': 'TAE',
    'tenis': 'TEN',
    'tenis de mesa': 'MES',
    'tiro': 'TIR',
    'triatlon': 'TRI',
    'navegacion a vela': 'NAV',
    'voley': 'VOL',
}

SEDES_SHORT = {
    'Stand Alone': 'SA',
    'Youth Olympic Park': 'YOP',
    'Green Park': 'GP',
    'Urban Park': 'UP',
    'Tecnopolis Park': 'TP',
}


ESPECIALISTAS = {
    'P1': set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES if x['deporte'] != 'baile'),
    'P2': set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES if x['deporte'] == 'baile' or x['categoria'] == 'C'),
    'P3': set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES if x['categoria'] in ('B', 'C')),
    'P4': set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES if x['categoria'] in ('A', 'D')),
    'P5': set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES if x['categoria'] in ('A', 'B')),
}

# Si posee especialistas -> lo puede cubrir
# Agrego ademas los que puede cubrir sin ser especialistas.
PUEDE_CUBRIR = {
    'P1': set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES),
    'P2': ESPECIALISTAS['P2'] | set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES if x['categoria'] == 'B'),
    'P3': ESPECIALISTAS['P3'] | set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES if x['categoria'] == 'A'),
    'P4': ESPECIALISTAS['P4'] | set(DEPORTES_SHORT[x['deporte']] for x in CONSTANTES if x['categoria'] == 'C'),
    'P5': ESPECIALISTAS['P5'],
}

class Evento(object):

    def __init__(self, **kw):
        self._id = kw['ID']
        self.sede = SEDES_SHORT[kw['SEDE']]
        self.dia = int(kw['DIA'])
        self.deporte = DEPORTES_SHORT[kw['DEPORTE'].lower()]
        self.start = kw['COMIENZO']
        self.end = kw['FIN']
        self.final = self.bool_final(kw['Final'])

    def short_name(self):
        return "{0.deporte}_{0._id}".format(self)

    @staticmethod
    def bool_final(si_no):
        return si_no == 'si'

    def __repr__(self):
        return repr(self.__dict__)

EVENTOS = [Evento(**x) for x in EVENTOS_RAW]

def puede_cubrir(periodista, deporte):
    return deporte in PUEDE_CUBRIR[periodista]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dias', type=int, help='La cantidad de dias')
    return parser.parse_args()

def output_deportes():
    print('set DEPORTES := ', ' '.join(DEPORTES_SHORT[d] for d in DEPORTES), ';')

def output_canales():
    print('set CANALES := ', ' '.join(CANALES), ';')

def output_periodistas():
    print('set PERIODISTAS := ', ' '.join(map(str, PERIODISTAS)), ';')

def output_sedes():
    print('set SEDES := ', ' '.join(SEDES_SHORT.values()), ';')

def output_dias(dias):
    print('set DIAS := ', ' '.join(map(str, range(1, dias+1))), ';')

def output_eventos(evts):
    print('set EVENTOS := ', ' '.join(e.short_name() for e in evts), ';')

def output_puede_cubrir(evts):
    # Header
    print('set PUEDE_CUBRIR : ', ' '.join(e.short_name() for e in evts), ':=')
    for p in PERIODISTAS:
        print(p, ' ', ' '.join(str(int(puede_cubrir(p, e.deporte))) for e in evts))
    print(';')

def parsear_opciones(dias):
    eventos = [ evento for evento in EVENTOS if evento.dia == 12 ]
    output_canales()
    output_dias(dias)
    output_deportes()
    output_sedes()
    output_periodistas()
    #output_eventos(eventos)
    #output_puede_cubrir(eventos)
    return eventos

def main():
    args = parse_args()
    parsear_opciones(args.dias)

if __name__ == '__main__':
    main()
