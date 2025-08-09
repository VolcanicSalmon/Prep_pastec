import sys
infile=open(sys.argv[1],'r')
reads={}
currline=''
record=[]
for line in infile.readlines():
    if line.startswith('>'):
        if currline!='':
            reads[currline]=''.join(record)
        currline=line 
        record=[]
    elif not line.startswith('>'):
        record.append(line)
reads[currline]=''.join(record)
infile.close()
filtered1={k:v for k,v in reads.items() if '? : ?' not in k}
filtered2={}
for k,v in filtered1.items():
    if not '?' in k:
        identifier=k.split(' : ')[0].split(' - ')[0]
        teclass=k.split(':')[0].split(' - ')[1]
        superfam=k.split(' : ')[2]
        fam=k.split(' : ')[1]
        newk=f'{identifier}#{teclass}/{fam}/{superfam}'
    else:
        identifier=k.split(' - ')[0].split(' - ')[0]
        teclass=k.split(':')[0].split(' - ')[1]
        fam=k.split(' : ')[1]
        newk=f'{identifier}#{teclass}/{fam}/Unknown\n'
    filtered2[newk]=v
outname=f"{sys.argv[1]}_filtered"
outfile=open(outname,'w')
for k, v in filtered2.items():
    outfile.write(k)
    outfile.write(v)
outfile.close()
