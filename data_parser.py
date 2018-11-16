from __future__ import print_function
import argparse
import csv
import time
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
HORAS = ['H{}'.format(n) for n in range(1, 56+1)]
CATEGORIAS = ['A', 'B', 'C', 'D', 'E']
DEPORTES = [x['deporte'] for x in CONSTANTES] # Mismo orden que el archivo
DATOS = {x['deporte']: x for x in CONSTANTES}
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
L_DEPORTES_SHORT = [DEPORTES_SHORT[d] for d in DEPORTES]

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
        self._deporte = kw['DEPORTE'].lower()
        self.deporte = DEPORTES_SHORT[kw['DEPORTE'].lower()]
        self.start = self.adjust_start(kw['COMIENZO'])
        self.end = self.adjust_end(kw['FIN'])
        self.final = self.bool_final(kw['Final'])

    def short_name(self):
        return "{0.deporte}_{0._id}".format(self)

    @staticmethod
    def bool_final(si_no):
        return si_no == 'si'

    @staticmethod
    def adjust_start(start):
        h, m = start.split(':')
        m = int(m)
        aux = [0, 15, 30, 45, 60]
        for i, _m in enumerate(aux):
            if m < _m:
                m = aux[i-1]
                break
        return "{}:{:02d}".format(h, m)

    @staticmethod
    def adjust_end(end):
        h, m = end.split(':')
        m = int(m)
        aux = [60, 45, 30, 15, 0]
        for i, _m in enumerate(aux):
            if m > _m:
                m = aux[i-1]
                break
        if m == 60:
            h = int(h) + 1
            m = 0
        return "{}:{:02d}".format(h, m)

    @staticmethod
    def get_bloque(timestamp):
        """
        Sabiendo que los bloques son de 15 minutos, comenzando a las 08:00 y finalizando a las
        22:00 debo obtener el numero de bloque
        """
        h, m = timestamp.split(':')
        return (4 * (int(h)-8)) + (int(m) / 15) + 1

    @property
    def calidad(self):
        return DATOS[self._deporte]['calidad']

    @property
    def calidad_final(self):
        return DATOS[self._deporte]['final']

    @property
    def calidad_especial(self):
        return DATOS[self._deporte]['especialista']

    def __repr__(self):
        return repr(self.__dict__)

EVENTOS = [Evento(**x) for x in EVENTOS_RAW]

def puede_cubrir(periodista, deporte):
    return deporte in PUEDE_CUBRIR[periodista]

def posee_especialista(periodista, deporte):
    return deporte in ESPECIALISTAS[periodista]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dias', type=int, help='La cantidad de dias')
    return parser.parse_args()

def output_deportes():
    print('set DEPORTES := ', ' '.join(DEPORTES_SHORT[d] for d in DEPORTES), ';')

def output_canales():
    print('set CANALES := ', ' '.join(CANALES), ';')

def output_horas():
    print('set HORAS :=', ' '.join(HORAS), ';')

def output_periodistas():
    print('set PERIODISTAS := ', ' '.join(map(str, PERIODISTAS)), ';')

def output_sedes():
    print('set SEDES := ', ' '.join(SEDES_SHORT.values()), ';')

def output_dias(dias):
    print('set DIAS := ', ' '.join(DIAS[:dias]), ';')

def output_eventos(evts):
    print('set EVENTOS := ', ' '.join(e.short_name() for e in evts), ';')

def output_param_bloques():
    print('param BLOQUES :=')
    for i, h in enumerate(HORAS):
        print(h, ' ', i+1)
    print(';')

def output_param_comienzo(eventos):
    print('param COMIENZO :=')
    for e in eventos:
        print(e.short_name(), ' ', e.get_bloque(e.start))
    print(';')

def output_param_fin(eventos):
    print('param FIN :=')
    for e in eventos:
        print(e.short_name(), ' ', e.get_bloque(e.end))
    print(';')

def output_param_calidad():
    print('param CALIDAD :=')
    for d in DEPORTES:
        print(DEPORTES_SHORT[d], ' ', DATOS[d]['calidad'])
    print(';')

def output_param_calidad_final():
    print('param AUMENTO_FINAL :=')
    for d in DEPORTES:
        print(DEPORTES_SHORT[d], ' ', DATOS[d]['final'])
    print(';')

def output_param_calidad_especial():
    print('param AUMENTO_ESPECIAL :=')
    for d in DEPORTES:
        print(DEPORTES_SHORT[d], ' ', DATOS[d]['especialista'])
    print(';')

def output_param_puede_cubrir():
    # Header
    print('param PUEDE_CUBRIR : ', ' '.join(L_DEPORTES_SHORT), ':=')
    for p in PERIODISTAS:
        print(p, ' ', ' '.join(str(int(puede_cubrir(p, d))) for d in L_DEPORTES_SHORT))
    print(';')

def output_param_especialista():
    # Header
    print('param ESPECIALISTA : ', ' '.join(L_DEPORTES_SHORT), ':=')
    for p in PERIODISTAS:
        print(p, ' ', ' '.join(str(int(posee_especialista(p, d))) for d in L_DEPORTES_SHORT))
    print(';')


def parsear_opciones(dias):
    eventos = [ evento for evento in EVENTOS if evento.dia == dias ]

    # Imprimo los sets
    output_dias(dias)
    output_canales()
    output_horas()
    output_deportes()
    output_sedes()
    output_periodistas()
    output_eventos(eventos)

    # Parametros que no cambian con los eventos
    #output_param_bloques()
    output_param_calidad()
    output_param_calidad_final()
    output_param_calidad_especial()
    output_param_puede_cubrir()
    output_param_especialista()

    # Parametos que cambian con los eventos
    output_param_comienzo(eventos)
    output_param_fin(eventos)
    return eventos

def main():
    args = parse_args()
    parsear_opciones(args.dias)

if __name__ == '__main__':
    main()
