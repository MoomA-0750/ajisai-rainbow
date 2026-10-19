import re,os,sys
from PIL import Image,ImageDraw,ImageFont
font=ImageFont.truetype(sys.argv[1],18)
out=Image.new('RGB',(1300,330))
for k,n in enumerate(['ajisai-rainbow','ajisai-rainbow-light']):
    t=open(os.path.join(os.path.dirname(__file__),'..','ghostty',n)).read()
    g=lambda key:re.search(r'\n'+key+r' = (#\w+)',t).group(1)
    p=dict(re.findall(r'palette = (\d+)=(#\w+)',t))
    x0=k*650; d=ImageDraw.Draw(out); d.rectangle([x0,0,x0+650,330],fill=g('background'))
    lines=[[(g('foreground'),n)],
      [(p['2'],'user@host'),(g('foreground'),':'),(p['4'],'~/project'),(p['5'],' (master)'),(g('foreground'),' $ git status')],
      [(p['1'],'  modified: '),(g('foreground'),'src/main.py')],
      [(p['2'],'  new file: '),(g('foreground'),'themes/rainbow.toml')],
      [(p['3'],'warning:'),(g('foreground'),' 1 commit ahead'),(p['8'],'  # comment')],
      [(p['6'],'def '),(p['4'],'ajisai'),(g('foreground'),'(sky='),(p['3'],'"rainbow"'),(g('foreground'),'): '),(p['5'],'return'),(p['1'],' 42')]]
    for i,l in enumerate(lines):
        x=x0+20
        for c,s in l: d.text((x,15+i*30),s,font=font,fill=c); x+=d.textlength(s,font=font)
    for i in range(16):
        d.rectangle([x0+20+(i%8)*76,205+(i//8)*55,x0+86+(i%8)*76,250+(i//8)*55],fill=p[str(i)])
out.save(sys.argv[2])
