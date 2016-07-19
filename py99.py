import sys,re,os

def _read_file(fin):
    c=None
    with open(fin,"r") as finf:
        c=finf.read()
    return c

def _write_file(fout,content):
    with open(fout,"w") as foutf:
        foutf.write(content)

fin=sys.argv[1]
fout=sys.argv[2]

content=_read_file(fin)

strings=[]
#Remove strings

ns_content=""
is_string=False
string_limiters=['"',"'"]
binded_limiter=None
for i,c in enumerate(content):
    if ((c==string_limiters[0] or c==string_limiters[1]) if binded_limiter==None else c==binded_limiter) and (i>1 and (content[i-1]!="\\" or (i>2 and content[i-2]=="\\"))):
        if is_string:
            ns_content+="@str$"+str(len(strings)-1)+"@"
            is_string=False
            binded_limiter=None
        else:
            strings.append("")
            is_string=True  
            binded_limiter=c
        ns_content+=c
    else:
        if not is_string:
            ns_content+=c
        else:
            strings[-1]+=c
content=ns_content

#Remove comments, we have only one type of comment that is // single line comment.
rx = re.compile(r'\/\/.*$')
lines=content.split("\n")
nl=[]
for i,l in enumerate(lines):
    nl.append(rx.sub("",l))
content="\n".join(nl)


# || -> or && -> and
rx = re.compile(r'\|\|', re.IGNORECASE|re.UNICODE)
content=rx.sub(" or ",content)
rx = re.compile(r'\&\&', re.IGNORECASE|re.UNICODE)
content=rx.sub(" and ",content)

# true -> True false -> False
rx = re.compile(r'([^A-Z0-9]|^)(true|false)')
content=rx.sub(lambda m: m.group(1)+m.group(2).title(),content)

# null -> None
rx = re.compile(r'([^A-Z0-9]|^)null')
content=rx.sub(lambda m:m.group(1)+"None",content)

# !abc -> not abc
rx = re.compile(r'\!([\s]*[A-Z\(]+)',re.IGNORECASE|re.UNICODE|re.MULTILINE)
content=rx.sub(lambda m:"not "+m.group(1),content)

# ; - > \n
rx = re.compile(r';[ ]*([A-Z0-9_])',re.IGNORECASE|re.UNICODE)
content=rx.sub(lambda m:";\n "+m.group(1),content)

#Clean curly brackets 
rx = re.compile(r'\)([\s]*)\{[ ]*\n',re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:"){",content)
rx = re.compile(r'\)([\s]*)\{',re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:"){\n",content)

rx = re.compile(r'\}([^\n\r]*[A-Z_])', re.IGNORECASE|re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:"}\n"+m.group(1),content)

#HACK: transform else in a function 
rx = re.compile(r'([^A-Z0-9]|^)else[\s]*\{',re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:m.group(1)+"else(){",content)

#HACK: transform try in a function 
rx = re.compile(r'([^A-Z0-9]|^)try[\s]*\{',re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:m.group(1)+"try(){",content)

#HACK: transform except in a function 
rx = re.compile(r'([^A-Z0-9]|^)except[\s]*\{', re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:m.group(1)+"except(){",content)

#Clean class
rx = re.compile(r'([^A-Z0-9]|^)class([A-Z0-9 _]+)\s*\{', re.IGNORECASE|re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:m.group(1)+"class"+m.group(2)+"(){",content)


#Remove spaces
rx = re.compile(r'^[ ]+',re.MULTILINE)
content=rx.sub("",content)
rx = re.compile(r'[ ]+$',re.MULTILINE)
content=rx.sub("",content)

#Replace curly brakets and apply correct indentation
indentation_level=0
lines=content.split("\n")
nl=[]
is_dict=[]
rx_space = re.compile("[\s\{]")
for i,l in enumerate(lines):
    lx=l
    for s in range(0,indentation_level*4):
        lx=" "+lx
    
    ly=""
    for k,c in enumerate(lx):
        if len(is_dict)<indentation_level :is_dict.append(False)
        i=indentation_level
        if c=="{":
            indentation_level+=1
            if k>1 and lx[k-1]==")": 
                if len(is_dict)<indentation_level :is_dict.append(False)
                is_dict[indentation_level-1]=False
                #print("Indentation >>")
                ly+=":"
                continue
            else: 
                if len(is_dict)<indentation_level :is_dict.append(False)
                is_dict[indentation_level-1]=True

             #   print("Is not a block [1]")

        elif c=="}":
        #    print("Indentation <<")
            if not is_dict[indentation_level-1]: 
                pass
            else:  
            #    print("Is not a block [2]")
                if len(is_dict)<indentation_level :is_dict.append(False)
                is_dict[indentation_level-1]=False
                ly+="}"
            indentation_level-=1    
            continue

        ly+=c
    nl.append(ly)
content="\n".join(nl)


#HACK: retransform try 
rx = re.compile(r'([^A-Z0-9]|^)try\(\)', re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:m.group(1)+"try",content)

#HACK: retransform else 
rx = re.compile(r'([^A-Z0-9]|^)else\(\)', re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:m.group(1)+"else",content)

#HACK: retransform except 
rx = re.compile(r'([^A-Z0-9]|^)except\(\)', re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:m.group(1)+"except",content)


def removeForBrakets(m):
    out=m.group(1)+m.group(2)+" ";
    rx = re.compile(r'\)([\s]*:)', re.UNICODE)
    out+=rx.sub(lambda x:x.group(1),m.group(3))
    return out

#HACK: Remove brackets from for
rx = re.compile(r'([^A-Z0-9]|^)(for[^\s]*)\(([^:]+\:)', re.IGNORECASE|re.MULTILINE|re.UNICODE)
content=rx.sub(lambda m:removeForBrakets(m),content)

#Add strings back
for i in range(0,len(strings)):
    content=content.replace("@str$"+str(i)+"@",strings[i])

_write_file(fout,content)