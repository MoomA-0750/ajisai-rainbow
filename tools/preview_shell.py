# Starship のプロンプトと lsd -l の出力（ANSI の色付き）を、暗い版・明るい版の配色で画像にする
# 使い方: python3 tools/preview_shell.py <等幅フォント> <ANSI のテキスト> <出力.png>
# Nerd Font の記号は描かず、Powerline の三角と半円だけ図形で描く
import re,os,sys
from PIL import Image,ImageDraw,ImageFont
font=ImageFont.truetype(sys.argv[1],18); bold=font
text=open(sys.argv[2],encoding='utf-8').read().rstrip('\n').split('\n')
cw=int(font.getlength('M')); lh=28; W=cw*max(len(re.sub(r'\x1b\[[0-9;]*m','',l)) for l in text)+40
out=Image.new('RGB',(W,(len(text)*lh+50)*2))
for k,n in enumerate(['ajisai-rainbow','ajisai-rainbow-light']):
    t=open(os.path.join(os.path.dirname(__file__),'..','ghostty',n)).read()
    g=lambda key:re.search(r'\n'+key+r' = (#\w+)',t).group(1)
    p={int(i):c for i,c in re.findall(r'palette = (\d+)=(#\w+)',t)}
    y0=k*(len(text)*lh+50); d=ImageDraw.Draw(out); d.rectangle([0,y0,W,y0+len(text)*lh+50],fill=g('background'))
    d.text((20,y0+6),n,font=font,fill=p[8])
    for i,line in enumerate(text):
        x=20; y=y0+36+i*lh; fg=bg=None; rev=False
        for tok in re.split(r'(\x1b\[[0-9;]*m)',line):
            m=re.fullmatch(r'\x1b\[([0-9;]*)m',tok)
            if m:
                a=[int(v) for v in m.group(1).split(';') if v] or [0]; j=0
                while j<len(a):
                    v=a[j]
                    if v==0: fg=bg=None; rev=False
                    elif v==7: rev=True
                    elif v==39: fg=None
                    elif v==49: bg=None
                    elif v in(38,48) and a[j+1]==5:
                        if v==38: fg=a[j+2]
                        else: bg=a[j+2]
                        j+=2
                    elif 30<=v<=37: fg=v-30
                    elif 40<=v<=47: bg=v-40
                    j+=1
                continue
            for ch in tok:
                f=p[fg] if fg is not None and fg<16 else g('foreground')
                b=p[bg] if bg is not None and bg<16 else g('background')
                if rev: f,b=b,f
                d.rectangle([x,y,x+cw,y+lh],fill=b)
                if ch=='': d.polygon([(x,y),(x+cw,y+lh/2),(x,y+lh)],fill=f)
                elif ch=='': d.pieslice([x-cw,y,x+cw,y+lh],270,90,fill=f)
                elif ch=='': d.pieslice([x,y,x+2*cw,y+lh],90,270,fill=f)
                elif not(0xe000<=ord(ch)<=0xf8ff or ord(ch)>=0xf0000): d.text((x,y+3),ch,font=font,fill=f)
                x+=cw
out.save(sys.argv[3])
