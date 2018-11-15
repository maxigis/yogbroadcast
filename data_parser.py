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

PERIODISTAS = [1, 2, 3, 4, 5]
CATEGORIAS = ['A', 'B', 'C', 'D', 'E']
DEPORTES = { x['deporte']: int(x['nro']) for x in CONSTANTES}
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
    1: set(x['deporte'] for x in CONSTANTES if x['deporte'] != 'baile'),
    2: set(x['deporte'] for x in CONSTANTES if x['deporte'] == 'baile' or x['categoria'] == 'C'),
    3: set(x['deporte'] for x in CONSTANTES if x['categoria'] in ('B', 'C')),
    4: set(x['deporte'] for x in CONSTANTES if x['categoria'] in ('A', 'D')),
    5: set(x['deporte'] for x in CONSTANTES if x['categoria'] in ('A', 'B')),
}

# Si posee especialistas -> lo puede cubrir
# Agrego ademas los que puede cubrir sin ser especialistas.
PUEDE_CUBRIR = {
    1: set(x['deporte'] for x in CONSTANTES),
    2: ESPECIALISTAS[2] | set(x['deporte'] for x in CONSTANTES if x['categoria'] == 'B'),
    3: ESPECIALISTAS[3] | set(x['deporte'] for x in CONSTANTES if x['categoria'] == 'C'),
    4: ESPECIALISTAS[4] | set(x['deporte'] for x in CONSTANTES if x['categoria'] == 'D'),
    5: ESPECIALISTAS[5],
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dias', type=int, help='La cantidad de dias')
    return parser.parse_args()

def parsear_opciones(dias):
    eventos = [ evento for evento in EVENTOS if evento.dia <= dias ]
    return eventos

def main():
    args = parse_args()
    parsear_opciones(args.dias)

if __name__ == '__main__':
    main()
