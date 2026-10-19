import re,os
def L(h):
    r,g,b=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    f=lambda c:c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
def cr(a,b):
    a,b=sorted([L(a),L(b)]);return (b+.05)/(a+.05)
for n in ['ajisai-rainbow','ajisai-rainbow-light']:
    t=open(os.path.join(os.path.dirname(__file__),'..','ghostty',n)).read(); bg=re.search(r'background = (#\w+)',t).group(1)
    print(n,'fg',round(cr(bg,re.search(r'\nforeground = (#\w+)',t).group(1)),1),' '.join(f"{i}:{cr(bg,c):.1f}" for i,c in re.findall(r'palette = (\d+)=(#\w+)',t)))
