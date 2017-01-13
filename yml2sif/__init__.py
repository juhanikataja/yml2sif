#!/usr/bin/python3

import yaml, argparse, sys, os, textwrap, collections

__dict_type__=collections.OrderedDict
__default_sw__=2

def yml2sif_version():
    return '0.2.4b1'

class Integer(yaml.YAMLObject):
    yaml_tag =u'!Integer'
    def __init__(self, data):
        if type(data) is list:
            self.data = [int(x) for x in data]
            self.len = len(data)
        else:
            self.data = int(data)
            self.len = 0

    def __repr__(self):
        if type(self.data) is list and type(self.data[0]) is int:
            s = "Integer"
            for k in self.data:
                s += ' '+keytostr(k)
            return(s)
        else:
            s = "Integer " + keytostr(self.data)
            return(s)
            

class Real(yaml.YAMLObject):

    yaml_tag =u'!Real'

    def __init__(self, data):
        if type(data) is list:
            self.data = [float(x) for x in data]
            self.len = len(data)
        else:
            self.data = float(data)
            self.len = 0

    def __repr__(self):
        if type(self.data) is list and type(self.data[0]) is float:
            s = "Real"
            for k in self.data:
                s += ' '+keytostr(k)
            return(s)
        else:
            s = "Real " + keytostr(self.data)
            return(s)


def keytostr(d):
    if type(d) is str:
        return '"'+d+'"'
    else:
        return str(d)

def write_indent(stream, indent, data):
    for i in range(0,indent):
        stream.write(' ')
    stream.writelines(data)

def write_sif_section(stream, key):
    sw = __default_sw__

    indent = 0
    write_indent(stream, indent*sw, [key[0],'\n'])

    indent += 1
    for sub in key[1].items():
        if type(sub[1]) is list:
            if sub[0].lower() == 'mesh db':
                write_indent(stream, indent*sw, [sub[0], ' '])
            else:
                write_indent(stream, indent*sw, [sub[0]+'('+str(len(sub[1]))+')', ' = '])

            data = [keytostr(x)+" " for x in sub[1][0:-1]]
            data.append(keytostr(sub[1][-1]))
            data.append('\n')
            write_indent(stream, 0, data)
            indent += 1
        elif type(sub[1]) is Integer or type(sub[1]) is Real:
            if sub[1].len > 0:
                write_indent(stream, indent*sw, [sub[0]+'('+str(sub[1].len)+')', ' = '])
            else:
                write_indent(stream, [indent*sw, sub[0], ' = '])
            write_indent(stream, 0, [str(sub[1]), '\n'])
            indent += 1
        else:
            write_indent(stream, indent*sw, [sub[0], ' = '])
            indent += 1
            write_indent(stream, 0, [str(sub[1]), '\n'])

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
            if type(key[1]) is list:
                siffile.write('Header\n')
                for K in key[1]:
                    write_indent(siffile, __default_sw__, [K,'\n'])
                siffile.write('End\n\n')
            else:
                write_sif_section(siffile, key)
            del sifdict[key[0]]
            break

    # then print rest in random order
    for key in sifdict.items():
        if type(key[1]) is __dict_type__:
            write_sif_section(siffile, key)

    try:
        siffile.writelines([sifdict['epilogue'], '\n'])
    except KeyError as ke:
        pass

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=__dict_type__):
    """Ordered loader for yaml from http://stackoverflow.com/a/21912744"""
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    def construct_Integer(loader,node):
        data = loader.construct_sequence(node)
        return Integer(data)

    def construct_Real(loader,node):
        data = loader.construct_sequence(node)
        return Real(data)

    OrderedLoader.add_constructor(
            u'!Integer',
            construct_Integer)

    OrderedLoader.add_constructor(
            u'!Real',
            construct_Real)

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    return yaml.load(stream, OrderedLoader)

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
  parser.add_argument('-k', '--key', metavar='key', type=str, help='print contents of ``key``.') 
  args = parser.parse_args()

  ymlfile = open(args.inputfile[0], 'r') if args.inputfile[0] != '-' else sys.stdin
  siffile = sys.stdout if args.outputfile == None else open(args.outputfile, 'w')

  ymldata = ordered_load(ymlfile.read(), yaml.SafeLoader)
  
  if args.key != None:
      siffile.write(ymldata[args.key])
      exit(0)

  dict_to_sif(ymldata, siffile)

if __name__  == '__main__':
    main()
