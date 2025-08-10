#needs troubleshooting for the option with gff
import argparse
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('-f','--format',type=int)
#format 1 is when only fasta is needed, format 2 is when headers need to be renamed after the coding annotation of the gff
parser.add_argument('-i','--infasta',type=str)
parser.add_argument('-g','--ingff',type=str)
parser.add_argument('-o','--output',type=str)
parser.add_argument('-s','--species',type=str)
args=parser.parse_args()
wicker_dict={'RIX':'LINE',
             'RXX':'RT/Unknown',
             'RIR':'LINE/R2',
             'RIT':'LINE/RTE',
             'RIJ':'LINE/Jockey',
             'RIL':'LINE:I',
             'RIP':'LINE/Pan',
             'RIC':'LINE/Chronos',
             'RSX':'SINE',
             'RST':'SINE/tRNA',
             'RSL':'SINE/7SL',
             'RSS':'SINE/5S',
             'RPX':'SINE/PLE',
             'RPP':'PLE/Penelope',
             'RLX':'LTR',
             'RLG':'LTR/Gypsy',
             'RLC':'LTR/Copia',
             'RLB':'LTR/Bel-Pao',
             'RLR':'LTR/Retrovirus',
             'RLE':'LTR/ERV',
             'RLA':'LTR/Halcyon',
             'RLH':'LTR/Echo',
             'RYX':'DIRS',
             'RYD':'DIRS/DIRS',
             'RYN':'DIRS/Ngaro',
             'RYY':'DIRS/VIPER',
             'DXX':'DNA',
             'DTX':'TIR',
             'DTT':'TIR/Tc1-Mariner',
             'DTA':'TIR/hAT',
             'DTM':'TIR/Mutator',
             'DTE':'TIR/Merlin',
             'DTR':'TIR/Transib',
             'DTP':'TIR/P',
             'DTB':'TIR/PiggyBac',
             'DTH':'PIF-Harbinger',
             'DTC':'TIR/CACTA',
             'DYX':'Crypton',
             'DYC':'Crypton/Crypton',
             'DHX':'Helitron',
             'DHH':'Helitron/Helitron',
             'DMX':'DNA/Maverick',
             'DMM':'Maverick/Maverick'
      }
def readargs():
    if args.format==1:
        outfile=write_fa_from_fa(args.infasta,args.output,args.species)
    elif args.format==2:
        outfile=write_fa_from_gff(args.infasta,args.ingff,args.species,args.output)
    else:
        exit(1)
def write_fa_from_fa(infasta,output,species):
    with open(infasta,'r') as infile, open(output,'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                for k,v in wicker_dict.items():
                    if line.find(k)==1:
                        line=line.rstrip()+'#'+v
                        break
                else:
                    line=line.rstrip()+'#Unknown\n'
                line=line.strip()+f" @{species}\n"
            outfile.write(line)
def write_fa_from_gff(infasta, ingff, species, output):
    fadict = {}
    with open(infasta, 'r') as fa:
        for line in fa:
            if line.startswith('>'):
                header = line.strip()
                sequence = next(fa).strip()
                fadict[header] = sequence

    print(f"FASTA dictionary: {fadict}")  # Debugging: Print the FASTA dictionary

    with open(ingff, 'r') as anno, open(output, 'w') as outfile:
        for annoline in anno:
            annoline = annoline.strip()
            print(f"Processing GFF line: {annoline}")  # Debugging: Print the current GFF line
            for header in fadict:
                if header in annoline:
                    print(f"Header found in GFF line: {header}")  # Debugging: Print the found header
                    codestringstart = annoline.find('TE_BLRtx ')
                    if codestringstart == -1:
                        codestring = 'Unknown'
                    else:
                        codestringend = annoline.find('\n', codestringstart)
                        if codestringend == -1:
                            codestringend = len(annoline)
                        codestring = annoline[codestringstart + len('TE_BLRtx '):codestringend].strip()
                        codestring = codestring.replace(':', '/')
                    newheader = header + '#' + codestring + ' @' + species + '\n'
                    outfile.write(newheader)
                    outfile.write(fadict[header] + '\n')
                    print(f"Written to output: {newheader}{fadict[header]}\n")  # Debugging: Print the written output
                    break

if __name__ == '__main__':
    readargs()
