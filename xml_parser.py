import argparse
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from operator import itemgetter

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='El XML generado por CPLEX', required=True)
    return parser.parse_args()

CANAL = "C(?P<canal>\d)"
EVENTO = "(?P<evt>.*)"
DIA = "D(?P<dia>\d+)"
EQUIPO = "P(?P<equipo>\d)"
SEDE = "(?P<sede>.*)"

class Cplex(object):
    regex_en_canal = "en_canal\({evento},{canal}\)".format(evento=EVENTO, canal=CANAL)
    regex_cubierto = "cubierto\({evento},{equipo}\)".format(evento=EVENTO, equipo=EQUIPO)
    regex_cubre_dia = "cubre\({equipo},{evento},H\d+,{dia}\)".format(equipo=EQUIPO, evento=EVENTO, dia=DIA)
    _regex_asignado = "asignado\({dia},{equipo},{sede}\)".format(dia=DIA, equipo=EQUIPO, sede=SEDE)


    def __init__(self):
        self.eventos = defaultdict(dict)
        self.asignados = defaultdict(dict)
        self.reg_set = [getattr(self, i) for i in dir(self) if i.startswith('regex_')]

    def match_asign(self, attrib):
        name = attrib['name']
        m = re.match(self._regex_asignado, name, re.IGNORECASE)
        if m:
            d = m.groupdict()
            equipo = d['equipo']
            dia = d['dia']
            sede = d['sede']
            # Clave compuesta
            key = "{}:{}".format(dia, equipo)
            self.asignados[key] = sede

    def match_gen(self, attrib):
        name = attrib['name']
        for regex in self.reg_set:
            m = re.match(regex, name, re.IGNORECASE)
            if m:
                d = m.groupdict()
                evt = d.get('evt')
                if 'dia' in d:
                    d['dia'] = int(d['dia'])
                self.eventos[evt].update(d)
                return
        self.match_asign(attrib)

    def get_sede(self, dia, equipo):
        key = "{}:{}".format(dia, equipo)
        return self.asignados[key]

    def parse(self, elem):
        #self.match_canal(elem)
        #self.match_cubierto(elem)
        self.match_gen(elem)

    def output(self):
        for k, v in self.eventos.iteritems():
            equipo = v['equipo']
            dia = v['dia']
            v['sede'] = self.get_sede(dia, equipo)

        sorted_evts = sorted(self.eventos.values(), key=itemgetter('dia'))
        for evt in sorted_evts:
            print "Dia: {dia}, evento: {evt}, equipo: {equipo}, sede: {sede}".format(**evt)


def navigate_xml(xml):
    root = ET.parse(xml).getroot()
    parser = Cplex()
    for var in root.iter('variables'):
        for child in var.getchildren():
            # Pueden haber errores de redondeo
            val = child.attrib['value']
            val = round(float(val))
            if val == 1:
                parser.parse(child.attrib)
    parser.output()


def main():
    args = parse_args()
    navigate_xml(args.file)

if __name__ == '__main__':
    main()
