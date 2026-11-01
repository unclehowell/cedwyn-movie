#!/usr/bin/env python3
"""door_art.py — Coming-soon door art for the Cedwyn documentary (1 Nov 2026, worker 72036582; owner's rule m:1d4eb2cf).
For every door not yet in manifest.json "filled": 960x540 WebP, background #f7f2e7, the Cedwyn estate silhouette (outline from
unclehowell/cedwyn branch estate-maps web/_cedwyn/parcels.json, read-only), River Ely, traced parcels, the place of the scene's
event marked (frames.json "parcels"; else the scene setting s01/s02/s11/s12 -> house & yard, s03 -> church; else the whole estate
outline dashed), "COMING SOON / Yn fuan / Próximamente", scene number, title and date. Output -> thumbs/soon/<id>.webp in the storage
repo unclehowell/cedwyn-movie (movie.js 1.9.0 reads it). Usage: python3 door_art.py frames.json manifest.json parcels.json OUTDIR — Sion's Tab agent"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont
frames=json.load(open(sys.argv[1])); man=json.load(open(sys.argv[2])); J=json.load(open(sys.argv[3])); OUT=sys.argv[4]
items=frames['items']; fm={f['n']:f for f in man.get('filled',[])}
outline=J['outline']['coords']; lats=[p[0] for p in outline]; lons=[p[1] for p in outline]
W_,H_=960,540; SC=2
BG=(247,242,231); INK=(46,58,50); SIL=(62,90,68); MARK=(163,58,42); RIV=(111,143,160); MUTE=(110,104,90)
FS='/home/user/.local/share/fonts/SourceSerif4.ttf'
lat0=51.4548; kx=math.cos(math.radians(lat0)); MX0,MY0,MW,MH=30,40,540,460
minx=min(lons)*kx; maxx=max(lons)*kx; miny=min(lats); maxy=max(lats); pad=0.08
S_=min(MW/((maxx-minx)*(1+2*pad)), MH/((maxy-miny)*(1+2*pad))); cx=(minx+maxx)/2; cy=(miny+maxy)/2; m_per_px=1/(S_/111320)
house=(J['house']['lat'],J['house']['lon']); church=(J['church']['lat'],J['church']['lon']); N94=(51.45272,-3.19883)
def font(sz,bold=False):
    try:
        f=ImageFont.truetype(FS,sz)
        try: f.set_variation_by_name('Bold' if bold else 'Regular')
        except Exception: pass
        return f
    except Exception: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif%s.ttf'%('-Bold' if bold else ''),sz)

def P(lat,lon): return (MX0+MW/2+(lon*kx-cx)*S_, MY0+MH/2-(lat-cy)*S_)

def wrap(d,text,f,maxw):
    words=text.split(); out=[]; cur=''
    for w in words:
        t2=(cur+' '+w).strip()
        if d.textlength(t2,font=f)<=maxw: cur=t2
        else:
            if cur: out.append(cur)
            cur=w
    if cur: out.append(cur)
    return out

def draw_art(f, loc):
    im=Image.new('RGB',(W_*SC,H_*SC),BG); d=ImageDraw.Draw(im)
    Q=lambda lat,lon:(P(lat,lon)[0]*SC,P(lat,lon)[1]*SC)
    lay=Image.new('RGBA',(W_*SC,H_*SC),(0,0,0,0)); dl=ImageDraw.Draw(lay)
    dl.line([Q(a,b) for a,b in J['river']['coords']],fill=RIV+(255,),width=5*SC,joint='curve')
    mask=Image.new('L',(W_*SC,H_*SC),0); ImageDraw.Draw(mask).rectangle([0,40*SC,575*SC,(H_-62)*SC],fill=255)
    im.paste(lay,(0,0),Image.composite(lay.split()[3],Image.new('L',lay.size,0),mask))
    d=ImageDraw.Draw(im)
    poly=[Q(a,b) for a,b in outline]; d.polygon(poly,fill=SIL)
    for tp in J['traced']: d.polygon([Q(a,b) for a,b in tp['coords']],outline=(150,175,150),width=1*SC)
    kind,label=loc['kind'],loc['label']
    if kind=='whole':
        pts=poly+[poly[0]]
        for i in range(len(pts)-1):
            (x1,y1),(x2,y2)=pts[i],pts[i+1]; L=math.hypot(x2-x1,y2-y1); n=max(1,int(L/(16*SC)))
            for k in range(0,n,2):
                a=k/n; b=min(1,(k+1)/n); d.line([(x1+(x2-x1)*a,y1+(y2-y1)*a),(x1+(x2-x1)*b,y1+(y2-y1)*b)],fill=MARK,width=6*SC)
    else:
        for (la,lo,rad_m) in loc['pts']:
            x,y=Q(la,lo); r=max(16,rad_m/m_per_px)*SC
            d.ellipse([x-r,y-r,x+r,y+r],outline=MARK,width=4*SC)
        for (la,lo,rad_m) in loc['pts'][:1]:
            x,y=Q(la,lo); ph=40*SC; pw=15*SC
            d.polygon([(x,y),(x-pw*0.95,y-ph+pw*0.2),(x+pw*0.95,y-ph+pw*0.2)],fill=MARK)
            d.ellipse([x-pw,y-ph-pw,x+pw,y-ph+pw],fill=MARK)
            d.ellipse([x-6*SC,y-ph-6*SC,x+6*SC,y-ph+6*SC],fill=BG)
    nx,ny=548*SC,70*SC
    d.polygon([(nx,ny-22*SC),(nx-8*SC,ny),(nx+8*SC,ny)],fill=INK); d.text((nx,ny+4*SC),'N',font=font(16*SC,True),fill=INK,anchor='mt')
    TX=605*SC; TW=330*SC
    d.line([(TX-22*SC,60*SC),(TX-22*SC,480*SC)],fill=(214,203,178),width=2*SC)
    y=70*SC
    d.text((TX,y),'COMING SOON',font=font(46*SC,True),fill=MARK); y+=60*SC
    d.text((TX,y),'Yn fuan · Próximamente',font=font(20*SC),fill=MUTE); y+=46*SC
    d.text((TX,y),'Scene %d'%f['n'],font=font(24*SC,True),fill=INK); y+=36*SC
    tf=font(27*SC,True); tl_=wrap(d,f['title'],tf,TW)
    if len(tl_)>3: tl_=tl_[:3]; tl_[-1]=tl_[-1].rstrip('.,;:')+'…'
    for ln in tl_: d.text((TX,y),ln,font=tf,fill=INK); y+=36*SC
    y+=8*SC
    for ln in wrap(d,f.get('date_range') or '',font(19*SC),TW)[:2]: d.text((TX,y),ln,font=font(19*SC),fill=MUTE); y+=26*SC
    lf=font(17*SC); cap=wrap(d,label,lf,560*SC)[:2]; yy=(H_-16-24*len(cap))*SC
    for ln in cap: d.text((MX0*SC,yy),ln,font=lf,fill=MUTE); yy+=24*SC
    d.text((MX0*SC,14*SC),'Cedwyn estate · Tŷ Mawr, Llandough',font=font(18*SC,True),fill=INK)
    return im.resize((W_,H_),Image.LANCZOS)

def locate(f):
    p=(f.get('parcels') or '').lower(); s=f.get('setting')
    if p:
        if 'n94' in p and 'churchyard' in p: return {'kind':'pts','pts':[(*N94,50),(*church,30)],'label':'Marked: the 1994 excavation ground north of the church, and the churchyard (±50 m)','src':'parcels'}
        if 'n94' in p: return {'kind':'pts','pts':[(*N94,50)],'label':'Marked: the 1994 excavation ground beside the house and yard, north of the church (±50 m)','src':'parcels'}
        if 'churchyard' in p: return {'kind':'pts','pts':[(*church,30)],'label':"Marked: St Dochdwy's churchyard, beside the estate (place not checked)",'src':'parcels'}
        if 'whole estate' in p: return {'kind':'whole','label':'Marked: the whole estate · the place within it is not checked yet','src':'parcels-whole'}
    if s in ('s01','s02','s11','s12'): return {'kind':'pts','pts':[(*house,25)],'label':'Marked: Tŷ Mawr, house and yard (from the scene setting; parcel not checked)','src':'setting:'+s}
    if s=='s03': return {'kind':'pts','pts':[(*church,30)],'label':"Marked: St Dochdwy's church and churchyard (from the scene setting)",'src':'setting:'+s}
    return {'kind':'whole','label':'Marked: the whole estate · the place within it is not checked yet','src':'unknown'+(':'+s if s else '')}

if __name__=='__main__':
    os.makedirs(OUT,exist_ok=True)
    for f in items:
        if f['n'] in fm: continue
        draw_art(f,locate(f)).save(os.path.join(OUT,f['id']+'.webp'),'WEBP',quality=80,method=4)
