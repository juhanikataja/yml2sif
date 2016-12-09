from yml2sif import dict_to_sif
from os import sys
import yaml


def test_dict_to_sif():
    ymlfile = open('./esim1.yml', 'r')
    siffile = sys.stdout

    ymldata = yaml.load(ymlfile.read())
    dict_to_sif(ymldata, siffile)
    ymlfile.close()

if __name__=="__main__":
    test_dict_to_sif()

