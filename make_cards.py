# coding=utf-8
# Social preview cards (1200x630 PNG) for avlinks hymn pages.
# Renders one card per requested hymn into cards/, referenced by the
# og:image meta that make_hymns_01.py emits when the PNG exists.
# Usage: python make_cards.py AVS2.html av01.001 av07.054 ...
import os,sys,subprocess
if hasattr(sys.stdout,'reconfigure'):
 sys.stdout.reconfigure(encoding='utf-8')
import make_hymns_01 as M

CHROME = os.environ.get('CHROME_BIN',
 '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
CARD_DIR = 'cards'
TMP_HTML = '_card_tmp.html'

CARD_TEMPLATE = u"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@font-face {{ font-family:'Sanskrit 2003'; src:url('fonts/sanskrit2003.ttf'); }}
@font-face {{ font-family:'Siddhanta'; src:url('fonts/siddhanta.ttf'); }}
html,body {{ margin:0; padding:0; }}
#card {{ width:1200px; height:630px; background:#ffffff; box-sizing:border-box;
 padding:60px 72px 52px; border-top:10px solid #1a3e6e;
 font-family:'Charis SIL','Gentium Plus',Georgia,'Times New Roman',serif;
 color:#1f2328; display:flex; flex-direction:column; }}
.badge {{ font-size:24px; color:#59636e; letter-spacing:0.5px; }}
h1 {{ margin:16px 0 0; font-size:66px; font-weight:bold; color:#1f2328; line-height:1.15; }}
.sub {{ font-size:30px; font-weight:normal; color:#59636e; }}
.sa {{ font-family:'Devanagari Sangam MN','Noto Serif Devanagari','Sanskrit 2003','Siddhanta',serif;
 font-size:46px; line-height:1.55; margin-top:30px; }}
.hn {{ font-size:34px; font-style:italic; color:#3d444d; margin-top:24px; }}
.footer {{ margin-top:auto; display:flex; justify-content:space-between;
 font-size:24px; color:#59636e; border-top:2px solid #d1d9e0; padding-top:18px; }}
</style></head>
<body><div id="card">
<div class="badge">sanskrit-lexicon.github.io/avlinks</div>
<h1>{title} <span class="sub">· {sub}</span></h1>
<div class="sa">{sa}</div>
<div class="hn">{hn}</div>
<div class="footer"><span>20 books · 731 hymns · 5933 verses</span><span>Translations by Dr. Mārcis Gasūns</span></div>
</div></body></html>
"""

def render(hymn):
 mandala,hymnnum = hymn.hymnid
 page = 'av%s.%s' %(mandala,hymnnum)
 sa = M.para_first_line(hymn.verses[0].verselines,'sa') or ''
 hn = M.para_first_line(hymn.verses[0].verselines,'hn') or ''
 html = CARD_TEMPLATE.format(
  title='AVŚ %s.%s' %(mandala,hymnnum),
  sub='Atharva Veda (Śaunakīya) · hymn %s.%s' %(mandala,hymnnum),
  sa=sa, hn=hn)
 with open(TMP_HTML,'w',encoding='utf-8') as f:
  f.write(html)
 out = os.path.join(CARD_DIR,page + '.png')
 if os.path.exists(out):
  os.remove(out)
 cmd = [CHROME,'--headless','--disable-gpu','--hide-scrollbars',
  '--allow-file-access-from-files','--window-size=1200,630',
  '--virtual-time-budget=3000','--screenshot=%s' % out,
  'file://%s' % os.path.abspath(TMP_HTML)]
 subprocess.run(cmd,capture_output=True,timeout=60,encoding='utf-8',errors='replace')
 if not os.path.exists(out) or os.path.getsize(out) == 0:
  print('CARD FAIL',page)
  return False
 print('card written:',out,os.path.getsize(out),'bytes')
 return True

if __name__ == '__main__':
 filein = sys.argv[1]
 ids = sys.argv[2:]
 if not ids:
  print('usage: python make_cards.py AVS2.html av01.001 [av02.001 ...]')
  exit(1)
 with open(filein,encoding='utf-8') as f:
  lines = [x.rstrip('\r\n') for x in f]
 verses = M.init_verses(M.adjust_lines1(lines))
 hymns = M.init_hymns(verses)
 byid = {'av%s.%s' % h.hymnid: h for h in hymns}
 os.makedirs(CARD_DIR,exist_ok=True)
 fails = []
 for id_ in ids:
  if id_ not in byid:
   print('unknown hymn id:',id_)
   fails.append(id_)
   continue
  if not render(byid[id_]):
   fails.append(id_)
 if os.path.exists(TMP_HTML):
  os.remove(TMP_HTML)
 if fails:
  print('FAILED:',','.join(fails))
  exit(1)
 print('%s cards OK' % len(ids))
