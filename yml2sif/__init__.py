#!/usr/bin/python3

import yaml, argparse, sys, os, textwrap, collections

def yml2sif_version():
    return '0.1.0'

def keytostr(d):
    if type(d) is str:
        return '"'+d+'"'
    else:
        return str(d)

def write_sif_section(stream, key):
    sw = 2
    def write_indent(stream, indent, data):
        for i in range(0,indent):
            stream.write(' ')
        stream.writelines(data)

    indent = 0
    write_indent(stream, indent*sw, [key[0],'\n'])

    indent += 1
    for sub in key[1].items():
        if not type(sub[1]) is list:
            write_indent(stream, indent*sw, [sub[0], ' = '])
            indent += 1
            write_indent(stream, 0, [str(sub[1]), '\n'])
        else:
            if sub[0].lower() == 'mesh db':
                write_indent(stream, indent*sw, [sub[0], ' '])
            else:
                write_indent(stream, indent*sw, [sub[0]+'('+str(len(sub[1]))+')', ' = '])

            indent += 1
            data = [keytostr(x)+" " for x in sub[1][0:-1]]
            data.append(keytostr(sub[1][-1]))
            data.append('\n')
            write_indent(stream, 0, data)
        indent -= 1
    indent -= 1
    stream.write('end\n\n')

def dict_to_sif(sifdict,siffile):

    siffile.write('! Generated with yml2sif version ')
    siffile.write(yml2sif_version())
    siffile.write('\n\n')

    # print prologue definitions on top
    try:
        siffile.writelines([sifdict['prologue'], '\n'])
    except KeyError as ke:
        pass

    # next print header
    for key in sifdict.items():
        if (key[0].lower() == 'header'):
            write_sif_section(siffile, key)
            del sifdict[key[0]]
            break

    # then print rest in random order
    for key in sifdict.items():
        if not type(key[1]) is str:
            write_sif_section(siffile, key)


    try:
        siffile.writelines([sifdict['epilogue'], '\n'])
    except KeyError as ke:
        pass


def main():
  parser = argparse.ArgumentParser(
      description=textwrap.dedent('''\
          Convert yml file to sif file assuming some structure

          Copyright (c) 2016 CSC - IT Center for Science

          Usage:

          Output order is the following:
            1. prologue definitions
            2. header section
            3. rest of the sections and their contents in random order'''),
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('inputfile', metavar='inputfile', type=str, nargs=1, help='YAML file to be converted.')
  parser.add_argument('outputfile', metavar='outputfile', type=str, nargs='?', help='If omitted, output is to stdout.')
  args = parser.parse_args()

  ymlfile = open(args.inputfile[0], 'r')
  siffile = sys.stdout if args.outputfile == None else open(args.outputfile, 'w')

  # This trick is from 
  # http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
  _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
  def dict_representer(dumper,data):
      return dumper.represent_dict(data.items())

  def dict_constructor(loader, node):
      return collections.OrderedDict(loader.construct_pairs(node))

  yaml.add_representer(collections.OrderedDict, dict_representer)
  yaml.add_constructor(_mapping_tag, dict_constructor)
  # Trick ends

  ymldata = yaml.load(ymlfile.read())

  dict_to_sif(ymldata, siffile)
