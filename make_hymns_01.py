# coding=utf-8
import sys,re,codecs
hymn_template =u"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>%s</title>
<link rel="stylesheet" type="text/css" href="avhymns.css">
</head>
<body>
%s
<div>
<hr/>
<span style="font-size:smaller">
Translations compiled by Dr. Mārcis Gasūns.
</span>
<br/>
</div>
<div style="height:900px"></div> <!-- a trick for proper anchor scrolling -->
</body>
</html>
"""
class Hymn(object):
 def __init__(self,hymnid,verses):
  self.hymnid = hymnid
  self.verses = verses
 def write(self,fileout):
  with codecs.open(fileout,"w","utf-8") as f:
   html = self.html()
   f.write(html + '\n')
 def html(self):
  mandala,hymnnum = self.hymnid
  title = "av%s.%s" %(mandala,hymnnum)
  bodylines = []
  for verse in self.verses:
   (_,_,versenum) = verse.verseid
   verselines = verse.verselines
   #print(title, len(verselines))
   for iline,line in enumerate(verselines):
    if iline == 0:
     # use id attribute for html5
     a = "<a id='av%s.%s.%s'/>" %(mandala,hymnnum,versenum)
     bodylines.append(a + line)
    else:
     bodylines.append(line)
  bodystring = '\n'.join(bodylines)
  htmlstring = hymn_template %(title,bodystring)
  return htmlstring

class Verse(object):
 def __init__(self,verseid,verselines):
  self.verseid = verseid
  self.verselines = verselines
  nlines = len(self.verselines)
  if nlines not in [5,6]:
   print('Verse error:',self.verseid,'has %s lines'%nlines)
   

def init_verses(lines):
 verses = []
 inverse = False
 for idx,line in enumerate(lines):
  m = re.search(r'^<p class="stamp">avś_([0-9]+)[.]([0-9]+)[.]([0-9]+)[.] </p>$',line)
  if idx == 0:
   # first verse
   if not m:
    #print("init_verses problem",idx,line.encode('utf-8'))
    print("init_verses problem",idx,line)
    exit(1)
   verseid = (m.group(1),m.group(2),m.group(3)) # keep as tuple for later
   verselines = [line]
   inverse = True
   continue
  if m:
   # first line of next verse found
   verse = Verse(verseid,verselines)
   verses.append(verse)
   # Start new verse
   verseid = (m.group(1),m.group(2),m.group(3)) # keep as tuple for later
   verselines = [line]
   inverse = True
   continue
  else:
   # add next line of current verse
   verselines.append(line)
 # install last verse
 verse = Verse(verseid,verselines)
 verses.append(verse)
 return verses

def init_hymns(verses):
 hymns = []
 for iverse,verse in enumerate(verses):
  (mandala,hymnnum,versenum) = verse.verseid
  if iverse == 0:
   # first hymn
   hymnid = (mandala,hymnnum)
   hymnverses = [verse]
  elif versenum == '01':
   # first line of next hymn
   hymn = Hymn(hymnid,hymnverses)
   hymns.append(hymn)
   # start next hymn
   hymnid = (mandala,hymnnum)
   hymnverses = [verse]
  else:
   # add another verse to current hymn
   hymnverses.append(verse)
 # install last hymn
 hymn = Hymn(hymnid,hymnverses)
 hymns.append(hymn)
 return hymns

def adjust_lines1(lines):
 ## keep only the lines that start with '<p '
 out = []
 for idx,x in enumerate(lines):
  if not x.startswith('<p '):
   continue
  if x.startswith('<p class="stamp">'):
   m = re.search(r'^(<p class="stamp">avś_[0-9]+[.][0-9]+[.][0-9]+[.]) (.*)</p>',x)
   if not m:
    print('adjust_lines1 error at line %s\n'%idx,x)
    exit(1)
   # remove some particular text in first line of each verse
   x = '%s </p>' % m.group(1)
  out.append(x)
 return out
if __name__ == "__main__":
 filein=sys.argv[1]
 dirout = sys.argv[2]
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"lines in",filein)
 outlines = adjust_lines1(lines)
 print(len(outlines),"adjusted lines")

 verses = init_verses(outlines)
 print(len(verses),"verses found")
 hymns = init_hymns(verses)
 print(len(hymns),"hymns found")
 # Write each hymn to a file
 for ihymn,hymn in enumerate(hymns):
  mandala,hymnnum = hymn.hymnid
  fileout = '%s/av%s.%s.html' %(dirout,mandala,hymnnum)
  hymn.write(fileout)
  #if ihymn == 5:
  # print("debug exit")
  # exit(1)
