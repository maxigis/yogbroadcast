import argparse
import re
import xml.etree.ElementTree as ET

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='El XML generado por CPLEX', required=True)
    return parser.parse_args()

class Cplex(object):
    en_canal_regex = "en_canal\((?P<evt>.*),C(?P<canal>\d)\)"

    def __init__(self):
        self.eventos = []

    def match_canal(self, attrib):

        if attrib['value'] != '0':
            return
        name = attrib['name']
        m = re.match(self.en_canal_regex, name, re.IGNORECASE)
        if m:
            d = m.groupdict()
            print "El evento {evt} se transmite por el canal {canal}".format(**d)

    def parse(self, elem):
        self.match_canal(elem)

def navigate_xml(xml):
    root = ET.parse(xml).getroot()
    parser = Cplex()
    for var in root.iter('variables'):
        for child in var.getchildren():
            parser.parse(child.attrib)


def main():
    args = parse_args()
    navigate_xml(args.file)

if __name__ == '__main__':
    main()
