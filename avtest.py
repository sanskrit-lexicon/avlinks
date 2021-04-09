# coding=utf-8
import sys,re,codecs
import unicodedata
def temp(filein,fileout):
 """ check for unknown unicode characters
 """
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 fout = codecs.open(fileout,"w","utf-8")
 nbad = 0
 for iline,line in enumerate(lines):
  lnum = iline+1
  out = "line#%s:%s" %(lnum,line)
  outarr = [out]
  #fout.write(out+'\n')
  badflag = False
  for ix,x in enumerate(line):
   try:
    name=unicodedata.name(x)
   except:
    name='UNKNOWN UNICODE'
    out = '%s:%s: %s %s %s '%(lnum,ix+1,ord(x),x,name)
    badflag = True
    outarr.append(out)
   #fout.write(out+'\n')
  #fout.write('\n')
  if badflag:
   for out in outarr:
    fout.write(out+'\n')
   nbad = nbad + 1
 fout.close()
 print(nbad,"lines with unknown unicode charcters written to",fileout)
def temp1():
 """ scratch function 
 """
 filein = "RV_sa-hn-ru-de-en.html"
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   lnum = iline+1
   if lnum == 128: break
  print(lnum)
  print(line.encode('utf-8'))
  for ix,x in enumerate(line):
   print(ix,x.encode('utf-8'),ord(x))
   if ord(x) == 57347:
    print("found bad character")
    exit(1)

def temp2old(filein,fileout):
 """ replace bad unicode character with a double-danda in line # 118518
 """
 
 fout = codecs.open(fileout,"w","utf-8")
 double_danda = u"\u0965"
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   outarr=[]
   found = False
   for ix,x in enumerate(line):
    if ord(x) == 57347:
     outarr.append(double_danda)
     found = True
    else:
     outarr.append(x)
   if found:
    out = ''.join(outarr)
    lnum = iline+1
    print("changed line #", lnum)
   else:
    out = line
   fout.write(out)
 fout.close()

def temp2(filein,fileout):
 """ replace bad unicode character with a double-danda in line # 118518
     Also, replace line-endings with unix line-end
 """
 
 fout = codecs.open(fileout,"w","utf-8")
 double_danda = u"\u0965"
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   lnum = iline+1
   line = line.rstrip('\r\n')
   if lnum == 119519:
    out = u" स॒मा॒नम॑स्तु वो॒ मनो॒ यथा॑ व॒ सुस॒हास॑ति॥</p>"
   else:
    out = line
   try:
    fout.write(out + '\n')
   except:
    print("problem at line # ",lnum)
    exit(1)
 fout.close()

def temp3():
 filein = "RV_sa-hn-ru-de-en_1.html"
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   lnum = iline+1
   #print(lnum)
   if lnum == 118535:
    print(line.encode('utf-8'))
    break
  exit(1)
  print(line.encode('utf-8'))
  for ix,x in enumerate(line):
   print(ix,x.encode('utf-8'),ord(x))
   if ord(x) == 57347:
    print("found bad character")
    exit(1)

# bad characters at line 118519
# स॒मा॒नम॑स्तु वो॒ मनो॒ यथा॑ व॒ सुस॒हास॑ति  </p> # \340\245

def temp4():
 filein = "RV_sa-hn-ru-de-en_1.html"
 fileout = "RV_sa-hn-ru-de-en_2.html"
 fout = codecs.open(fileout,"w","utf-8")
 nfound = 0
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   line = line.rstrip('\r\n')
   lnum = iline+1
   out = []
   found = False
   for ix,x in enumerate(line):
    #print(ix,x.encode('utf-8'),ord(x))
    if ord(x) == 57347:
     found = True
     y = u"\u0903"  # visarga
     out.append(y)
    else:
     out.append(x)
   if found:
    outline = ''.join(out)
    nfound = nfound + 1
   else:
    outline = line
   fout.write(outline + '\n')
 fout.close()
 print(nfound,"bad visargas changed")
 print(lnum,"lines read from",filein)
 print(lnum,"lines written to",fileout)

def temp5(filein,fileout):
 #filein = "RV_sa-hn-ru-de-en_1.html"
 #fileout = "RV_sa-hn-ru-de-en_3.html"
 fout = codecs.open(fileout,"w","utf-8")
 nfound = 0
 visarga = u"\u0903"
 udatta = u"\u0951"
 anudatta = u"\u0952"
 ordudatta = 2385
 ordanudatta = 2386
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   #line = line.rstrip('\r\n')
   lnum = iline+1
   out = []
   found = False
  
   for ix,x in enumerate(line):
    if ord(x) == 57347:
     # 2385 is udAtta , 2386 is anudAtta
     xprev = line[ix-1]
     if ord(xprev) in [ordudatta,ordanudatta]:
      # put visarga, then accent
      prev = out.pop()  # udatta or anudatta
      out.append(visarga)
      out.append(prev)
     else:
      print("Unexpected char before bad visarga %s" %(ord(xprev)))
      print("@ line",lnum)
      exit(1)
     found = True
     #out.append(y)
    else:
     out.append(x)
   if found:
    outline = ''.join(out)
    nfound = nfound + 1
   else:
    outline = line
   #fout.write(outline + '\n')
   fout.write(outline)
 fout.close()
 print(nfound,"bad visargas changed")
 print(lnum,"lines read from",filein)
 print(lnum,"lines written to",fileout)

def temp6(filein,fileout):
 # Two additional adjustments:
 # digit 1 + 57353 + 57351 -> 
 # 2407 + 2386 + 2385 = 
 # DEVANAGARI DIGIT ONE + ANUDATTA + UDATTA
 # digit 3 + 57353 + 57351 ->
 # DEVANAGARI DIGIT THREE + ANUDATTA + UDATTA
 
 #filein = "RV_sa-hn-ru-de-en_3.html"
 #fileout = "RV_sa-hn-ru-de-en_4.html"
 fout = codecs.open(fileout,"w","utf-8")
 nfound = 0
 visarga = u"\u0903"
 udatta = u"\u0951"
 anudatta = u"\u0952"
 devaOne = u"\u0967"
 devaThree = u"\u0969"
 ordudatta = 2385
 ordanudatta = 2386
 counter = {}
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   #line = line.rstrip('\r\n')
   lnum = iline+1
   out = []
   found = False
   n = len(line)
   for ix,x in enumerate(line):
    if x in ['1','3'] and (ix+2<n) and(ord(line[ix+1])==57353) and (ord(line[ix+2])==57351):
     found = True
     if x == '1':
      out.append(devaOne)
     else:
      out.append(devaThree)
     out.append(anudatta)
     out.append(udatta)
    elif ord(x) in [57353,57351]:
     # skip these
     pass
    else:
     out.append(x)
   if found:
    outline = ''.join(out)
    nfound = nfound + 1
   else:
    outline = line
   #fout.write(outline + '\n')
   fout.write(outline)
 fout.close()
 for o in counter:
  print(o,counter[o])
 #return
 print(nfound,"lines changed")
 print(lnum,"lines read from",filein)
 print(lnum,"lines written to",fileout)

def temp7(filein,fileout):
 fout = codecs.open(fileout,"w","utf-8")
 nfound = 0
 with codecs.open(filein,"r","utf-8") as f:
  lnum = 0
  for iline,line in enumerate(f):
   line = line.rstrip('\r\n')
   lnum = lnum + 1
   if '\r' in line:
    line = line.replace('\r','')
    nfound = nfound + 1
   fout.write(line + '\n')
 #return
 print(nfound,"lines changed with intermediate carriage returns")
 print(lnum,"lines read from",filein)
 print(lnum,"lines written to",fileout)

if __name__ == "__main__":
 option = sys.argv[1]
 if option == '0':
  temp(sys.argv[2],sys.argv[3])
 elif option == '2':
  temp2(sys.argv[2],sys.argv[3])
 elif option == '3':
  temp3()
 elif option == '4':
  temp4()
 elif option == '5':
  temp5(sys.argv[2],sys.argv[3])
 elif option == '6':
  temp6(sys.argv[2],sys.argv[3])
 elif option == '7':
  temp7(sys.argv[2],sys.argv[3])
 else:
  print("unknown option")
