import json,os,urllib.request as R
U=os.environ["MAKEFUN_ENV_URL"];F="abcdefgh"
def P(p,b):return json.load(R.urlopen(U+p,json.dumps(b).encode()))
V=[0,100,320,330,500,900,0];K=[-33,-31,-18,-14,14,18,31,33];G=[-17,-16,-15,-1,1,15,16,17];B=[-17,-15,15,17];O=[-16,-1,1,16]
def o(t):return 0<=t<128 and not t&136
def A(b,s,w):
 p=1 if w else -1
 for t in (s-15,s-17) if w else (s+15,s+17):
  if o(t) and b[t]==p:return 1
 for d in K+G:
  t=s+d
  if o(t) and ((d in K and b[t]==2*p) or (d in G and b[t]==6*p)):return 1
 for d in B:
  t=s+d
  while o(t):
   x=b[t]
   if x:
    if x==3*p or x==5*p:return 1
    break
   t+=d
 for d in O:
  t=s+d
  while o(t):
   x=b[t]
   if x:
    if x==4*p or x==5*p:return 1
    break
   t+=d
 return 0
def M(b,w,c):
 m=[]
 for s in range(128):
  if s&136:continue
  x=b[s]
  if not x or (x>0)!=w:continue
  a=abs(x)
  if a==1:
   d=16 if w else -16;t=s+d
   if o(t) and not b[t]:
    if t>>4 in (0,7):m.append((s,t,5))
    else:
     m.append((s,t,0))
     if (s>>4)==(1 if w else 6):
      t2=s+2*d
      if not b[t2]:m.append((s,t2,0))
   for dt in (d-1,d+1):
    t=s+dt
    if o(t):
     y=b[t]
     if y and (y>0)!=w:
      if t>>4 in (0,7):m.append((s,t,5))
      else:m.append((s,t,0))
  elif a==2 or a==6:
   for d in (K if a==2 else G):
    t=s+d
    if o(t):
     y=b[t]
     if not y or (y>0)!=w:m.append((s,t,0))
  else:
   for d in (B if a==3 else O if a==4 else B+O):
    t=s+d
    while o(t):
     y=b[t]
     if not y:m.append((s,t,0))
     else:
      if (y>0)!=w:m.append((s,t,0))
      break
     t+=d
 for w2,rr,k,r,ee,pp,d in ((1,"K",4,7,(5,6),(4,5,6),6),(1,"Q",4,0,(1,2,3),(4,3,2),2),(0,"k",116,119,(117,118),(116,117,118),118),(0,"q",116,112,(113,114,115),(116,115,114),114)):
  if w2==w and rr in c and not any(b[i] for i in ee) and b[k]==(6 if w else -6) and b[r]==(4 if w else -4) and not any(A(b,i,not w) for i in pp):m.append((k,d,0))
 return m
def D(b,w,c,s,t,p):
 n=b[:];x=n[s];n[s]=0;n[t]=p if p else x
 if abs(x)==6 and abs(t-s)==2:
  if t>s:n[s+3]=0;n[s+1]=4 if x>0 else -4
  else:n[s-4]=0;n[s-1]=4 if x>0 else -4
 nc=c
 if abs(b[s])==6:nc=nc.replace("K","").replace("Q","") if w else nc.replace("k","").replace("q","")
 for a,z in ((0,"Q"),(7,"K"),(112,"q"),(119,"k")):
  if s==a or t==a:nc=nc.replace(z,"")
 return n,nc
def L(b,w,c):
 r=[]
 for s,t,p in M(b,w,c):
  n,nc=D(b,w,c,s,t,p)
  if not A(n,n.index(6 if w else -6),not w):r.append((s,t,p,n,nc))
 return r
def E(b):
 s=0
 for i,x in enumerate(b):
  if x:
   f=i&7;r=i>>4;a=abs(x)
   z=((r if x>0 else 7-r)**2) if a==1 else (3-abs(f-3.5))*7+(3-abs(r-3.5))*5 if a<4 else (3-abs(f-3.5))*2 if a<6 else -((r if x>0 else 7-r))*4
   s+=V[a]+z if x>0 else -(V[a]+z)
 return s
class X(Exception):pass
def Q(b,w,c,al,be,d):
 global N;N+=1
 if N>6e4:raise X
 st=E(b) if w else -E(b)
 if d<=0:return st
 if st>=be:return be
 if st>al:al=st
 for s,t,p,n,nc in L(b,w,c):
  if not b[t] and not p:continue
  sc=-Q(n,not w,nc,-be,-al,d-1)
  if sc>=be:return be
  if sc>al:al=sc
 return al
def S(b,w,c,d,al,be):
 global N;N+=1
 if N>6e4:raise X
 if d==0:return Q(b,w,c,al,be,2)
 ms=L(b,w,c)
 if not ms:return -99990*A(b,b.index(6 if w else -6),not w)
 ms.sort(key=lambda m:-V[abs(b[m[1]])])
 y=-999999
 for s,t,p,n,nc in ms:
  sc=-S(n,not w,nc,d-1,-be,-al)
  if sc>y:y=sc
  if y>al:al=y
  if al>=be:break
 return y
def Y(fen):
 p=fen.split();b=[0]*128;r=7;f=0
 for ch in p[0]:
  if ch=="/":r-=1;f=0
  elif ch.isdigit():f+=int(ch)
  else:
   v="PNBRQK".index(ch.upper())+1;b[r*16+f]=v if ch.isupper() else -v;f+=1
 w=p[1]=="w";c=p[2].replace("-","")
 return b,w,c
def C(fen,legal):
 global N;b,w,c=Y(fen);best=legal[0]
 N=0
 for d in (2,3,4):
  try:
   cur=legal[0];cs=-999999
   for mv in legal:
    s=F.index(mv[0])+(int(mv[1])-1)*16;t=F.index(mv[2])+(int(mv[3])-1)*16;p=5 if len(mv)==5 else 0
    n,nc=D(b,w,c,s,t,p);sc=-S(n,not w,nc,d-1,-999999,999999)
    if sc>cs:cs=sc;cur=mv
   best=cur
  except X:break
 return best
while True:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=P("/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"])})
