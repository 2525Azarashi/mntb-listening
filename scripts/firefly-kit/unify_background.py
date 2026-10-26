#!/usr/bin/env python3
"""
とびら君 C動画（Firefly の5秒書き出し）を、アプリ用の 720×720・クリーム背景・1MB未満に取り込む道具。
  ・緑背景 → 色で切り抜いてクリーム色 #FBF5E8 に（緑のにじみを消し、床に薄い影）
  ・肌色／茶色の背景 → 背景だけクリーム色に塗り替え（plain）。複雑な背景は GrabCut（grab）
  ・mode='none' は背景を触らない（UR の夜空・金色など演出の背景）
  ・Firefly が最初と最後に貼る参照画像のコマは、CLIPS の区間（ss〜to）で切り落とす
使い方：
  元動画を SRC に v00.mp4 … の名前で置き、CLIPS の区間を合わせてから
  python3 scripts/firefly-kit/unify_background.py C01 C02 …   → OUT に <name>.mp4 と <name>-poster.webp
  （できたものを public/cinematics/ にコピーし、docs/CINEMATICS.md の表を更新）
必要：python3・numpy・opencv-python・ffmpeg。メモリ 1GB でも動くよう1本ずつ処理する。
2026-10-26 に使った元動画の対応：v99=C01 v03=C02 w16=C03 w18=C04 v08=C05 v07=C06 v00=C07 v01=C08 v02=C09
  w17=C10 w19=C11 v11=C12 v12=C13 v13=C14 v14=C15 w20=C16
"""
import os, sys
SRC = os.environ.get('FIREFLY_SRC', '.tmpwork/firefly_src')
OUT = os.environ.get('FIREFLY_OUT', '.tmpwork/cinematics_out')
os.makedirs(OUT, exist_ok=True)
import cv2, numpy as np, subprocess, json
S=720
CREAM=np.array([0xFB,0xF5,0xE8],np.float32)
def read(v):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f'{SRC}/{v}.mp4','-vf',f'scale={S}:{S}:flags=lanczos','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,S,S,3)
yy,xx=np.mgrid[0:S,0:S].astype(np.float32)/S
BASIS=np.stack([np.ones_like(xx),xx,yy,xx*yy,xx*xx,yy*yy],-1).reshape(-1,6)
BAND=np.zeros((S,S),bool); b=int(S*0.05); BAND[:b]=BAND[-b:]=True; BAND[:,:b]=BAND[:,-b:]=True
def greenmask(img):
    hsv=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
    h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    f=img.astype(np.int16); gs=f[...,1]-np.maximum(f[...,0],f[...,2])
    return ((h>=33)&(h<=90)&(s>70)&(v>35)&(gs>18)), gs
def bgmodel(lab,G):
    m=(BAND&~G).reshape(-1)
    if m.sum()<500: return None
    X=BASIS[m]; Y=lab.reshape(-1,3)[m]
    # robust: two passes
    c,_,_,_=np.linalg.lstsq(X,Y,rcond=None)
    r=np.abs(X@c-Y).sum(1); k=r<np.percentile(r,70)
    c,_,_,_=np.linalg.lstsq(X[k],Y[k],rcond=None)
    return (BASIS@c).reshape(S,S,3)
def matte(img, plain=True):
    G,gs=greenmask(img)
    lab=cv2.cvtColor(cv2.GaussianBlur(img,(3,3),0),cv2.COLOR_RGB2LAB).astype(np.float32)
    cand=G.copy()
    if plain:
        M=bgmodel(lab,G)
        if M is not None:
            dL=lab[...,0]-M[...,0]; dab=np.sqrt(((lab[...,1:]-M[...,1:])**2).sum(-1))
            cand|=(dab<7)&(dL>-38)&(dL<10)
    cand=cv2.morphologyEx(cand.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    # connect to border (or to green, which is always bg)
    n,lbl=cv2.connectedComponents(cand,connectivity=4)
    border=np.unique(np.concatenate([lbl[0],lbl[-1],lbl[:,0],lbl[:,-1]]))
    keep=np.zeros(n,bool); keep[border]=True
    gl=np.unique(lbl[G&(cand>0)]); keep[gl]=True; keep[0]=False
    bg=keep[lbl]
    # fill tiny fg islands (noise) inside bg
    fg=(~bg).astype(np.uint8)
    n2,l2,st,_=cv2.connectedComponentsWithStats(fg,connectivity=8)
    small=st[:,cv2.CC_STAT_AREA]<120; small[0]=False
    fg[small[l2]&(l2>0)]=0
    # dark green fringe around keyed area -> bg
    near=cv2.dilate((~fg.astype(bool)).astype(np.uint8),np.ones((5,5),np.uint8))>0
    fg[near&(gs>6)&(fg>0)]=0
    a=cv2.GaussianBlur(fg.astype(np.float32),(0,0),1.1)
    a=np.clip((a-0.15)/0.7,0,1)
    F=img.astype(np.float32).copy()
    gmax=np.maximum(F[...,0],F[...,2]); spill=np.maximum(F[...,1]-gmax-4,0)
    F[...,1]-=spill; F[...,0]+=spill*0.25; F[...,2]+=spill*0.25
    # edge: blend fringe toward cream to kill old-bg halo
    edge=(a<0.98)[...,None]
    F=np.where(edge, F*0.75+CREAM*0.25*(1-a[...,None])+F*0.25*a[...,None], F)
    return np.clip(F,0,255),a
def shadow(cx,w,floor,strength=0.20):
    sw=max(w,80)*0.55; sh=sw*0.14
    e=((xx*S-cx)/sw)**2+((yy*S-floor)/sh)**2
    return np.clip(1-e,0,1)**1.5*strength
def comp(F,a,sh=None):
    bg=np.ones((S,S,3),np.float32)*CREAM
    if sh is not None: bg=bg*(1-sh[...,None])+np.array([160,140,112],np.float32)*sh[...,None]
    return (F*a[...,None]+bg*(1-a[...,None])).astype(np.uint8)

CREAM_LAB=cv2.cvtColor(np.uint8([[[0xFB,0xF5,0xE8]]]),cv2.COLOR_RGB2LAB)[0,0].astype(np.float32)
def bodymask(lab,M,G):
    dL=lab[...,0]-M[...,0]; dab=np.sqrt(((lab[...,1:]-M[...,1:])**2).sum(-1))
    strong=((dab>13)|(dL<-55)|(dL>14))&~G
    strong=cv2.morphologyEx(strong.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    n,l,st,_=cv2.connectedComponentsWithStats(strong,connectivity=8)
    keep=st[:,cv2.CC_STAT_AREA]>=900; keep[0]=False
    m=keep[l].astype(np.uint8)
    # fill holes
    ff=m.copy(); h=np.zeros((S+2,S+2),np.uint8)
    inv=(1-m).astype(np.uint8); cv2.floodFill(inv,h,(0,0),0)
    m=m|inv
    return m,dL,dab
def unify(img, plain=True, shadow_for_green=True):
    """Return frame with background unified to cream. plain: bg is a smooth tan/cream (recolor)."""
    G,gs=greenmask(img)
    G=cv2.dilate(G.astype(np.uint8),np.ones((3,3),np.uint8))>0 if G.any() else G
    labu=cv2.cvtColor(img,cv2.COLOR_RGB2LAB).astype(np.float32)
    lab=cv2.GaussianBlur(labu,(0,0),1.0)
    out=labu.copy()
    M=bgmodel(lab,G) if plain else None
    if M is not None:
        body,dL,dab=bodymask(lab,M,G)
        soft=cv2.GaussianBlur(cv2.dilate(body,np.ones((3,3),np.uint8)).astype(np.float32),(0,0),2.0)
        w=(1-soft)
        out[...,0]+= (CREAM_LAB[0]-M[...,0])*w
        wc=w*np.clip(1-(dab-10)/30,0.35,1)
        out[...,1]+= (CREAM_LAB[1]-M[...,1])*wc
        out[...,2]+= (CREAM_LAB[2]-M[...,2])*wc
    rgb=cv2.cvtColor(np.clip(out,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB).astype(np.float32)
    if G.sum()>50:
        g0,_=greenmask(img)
        # alpha from green key
        fg=(~(cv2.morphologyEx(g0.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))>0)).astype(np.uint8)
        n2,l2,st,_=cv2.connectedComponentsWithStats(1-fg,connectivity=8)
        fg2=fg.copy()
        near=cv2.dilate((1-fg),np.ones((5,5),np.uint8))>0
        fg2[near&(gs>8)]=0
        a=cv2.GaussianBlur(fg2.astype(np.float32),(0,0),1.0); a=np.clip((a-0.15)/0.7,0,1)
        gmax=np.maximum(rgb[...,0],rgb[...,2]); spill=np.maximum(rgb[...,1]-gmax-4,0)
        rgb[...,1]-=spill; rgb[...,0]+=spill*0.3; rgb[...,2]+=spill*0.3
        bg=np.ones((S,S,3),np.float32)*CREAM
        if shadow_for_green:
            ys,xs=np.where(a>0.6)
            if len(ys)>500:
                fy=np.percentile(ys,99.7); x0,x1=np.percentile(xs,[3,97])
                sh=shadow((x0+x1)/2,x1-x0,fy-4,0.16)
                bg=bg*(1-sh[...,None])+np.array([160,140,112],np.float32)*sh[...,None]
        # only replace where green (a<1); keep recolored rest
        rgb=rgb*a[...,None]+bg*(1-a[...,None])
    return np.clip(rgb,0,255).astype(np.uint8)

def unify2(img, prev=None):
    """GrabCut-based: robust for vignette/complex bgs."""
    G,gs=greenmask(img)
    labu=cv2.cvtColor(img,cv2.COLOR_RGB2LAB).astype(np.float32)
    lab=cv2.GaussianBlur(labu,(0,0),1.0)
    M=bgmodel(lab,G)
    body,dL,dab=bodymask(lab,M,G)
    s=360; k=S//s
    small=cv2.resize(img,(s,s),interpolation=cv2.INTER_AREA)
    gm=np.full((s,s),cv2.GC_PR_BGD,np.uint8)
    bs=cv2.resize(body,(s,s),interpolation=cv2.INTER_NEAREST)
    gm[cv2.erode(bs,np.ones((9,9),np.uint8))>0]=cv2.GC_PR_FGD
    if prev is not None:
        pv=cv2.resize(prev,(s,s),interpolation=cv2.INTER_NEAREST)
        gm[cv2.erode(pv,np.ones((11,11),np.uint8))>0]=cv2.GC_PR_FGD
    gm[:4]=gm[-4:]=gm[:,:4]=gm[:,-4:]=cv2.GC_BGD
    Gs=cv2.resize(G.astype(np.uint8),(s,s),interpolation=cv2.INTER_NEAREST)>0
    gm[Gs]=cv2.GC_BGD
    bgd=np.zeros((1,65),np.float64); fgd=np.zeros((1,65),np.float64)
    cv2.grabCut(cv2.cvtColor(small,cv2.COLOR_RGB2BGR),gm,None,bgd,fgd,4,cv2.GC_INIT_WITH_MASK)
    fg=((gm==cv2.GC_FGD)|(gm==cv2.GC_PR_FGD)).astype(np.uint8)
    n,l,st,_=cv2.connectedComponentsWithStats(fg,connectivity=8)
    keep=st[:,cv2.CC_STAT_AREA]>=200; keep[0]=False; fg=keep[l].astype(np.uint8)
    inv=(1-fg).astype(np.uint8); h=np.zeros((s+2,s+2),np.uint8); cv2.floodFill(inv,h,(0,0),0); fg|=inv
    fgL=cv2.resize(fg,(S,S),interpolation=cv2.INTER_LINEAR)
    # plate: inpaint bg at low-res
    ps=90; sm=cv2.resize(labu,(ps,ps),interpolation=cv2.INTER_AREA)
    hole=cv2.dilate(cv2.resize(fg,(ps,ps),interpolation=cv2.INTER_NEAREST),np.ones((3,3),np.uint8))
    hole|=cv2.resize(G.astype(np.uint8),(ps,ps),interpolation=cv2.INTER_NEAREST)
    sm8=np.clip(sm,0,255).astype(np.uint8)
    pl=cv2.inpaint(sm8,hole*255,5,cv2.INPAINT_TELEA).astype(np.float32)
    pl=cv2.GaussianBlur(pl,(0,0),3)
    P=cv2.resize(pl,(S,S),interpolation=cv2.INTER_CUBIC)
    soft=cv2.GaussianBlur(fgL.astype(np.float32),(0,0),1.5)
    w=1-soft
    out=labu.copy()
    d=np.sqrt(((labu[...,1:]-P[...,1:])**2).sum(-1))
    wc=w*np.clip(1-(d-10)/30,0.35,1)
    out[...,0]+=(CREAM_LAB[0]-P[...,0])*w
    out[...,1]+=(CREAM_LAB[1]-P[...,1])*wc
    out[...,2]+=(CREAM_LAB[2]-P[...,2])*wc
    rgb=cv2.cvtColor(np.clip(out,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB).astype(np.float32)
    if G.sum()>50:
        a=cv2.GaussianBlur((~G).astype(np.float32),(0,0),1.0)
        near=cv2.dilate(G.astype(np.uint8),np.ones((5,5),np.uint8))>0
        a[near&(gs>8)]=0
        gmax=np.maximum(rgb[...,0],rgb[...,2]); spill=np.maximum(rgb[...,1]-gmax-4,0)
        rgb[...,1]-=spill; rgb[...,0]+=spill*0.3; rgb[...,2]+=spill*0.3
        rgb=rgb*a[...,None]+CREAM*(1-a[...,None])
    return np.clip(rgb,0,255).astype(np.uint8), fg

# id, src, start, end, mode, speed, extra
CLIPS={
 'C01':dict(src='v99',ss=2.70,to=5.00,mode='plain',name='title'),
 'C02':dict(src='v03',ss=0.25,to=3.00,mode='plain',name='attack'),
 'C05':dict(src='v08',ss=2.20,to=3.75,mode='green',name='gacha_n',glow=(255,250,225),gl=0.45),
 'C06':dict(src='v07',ss=3.00,to=5.00,mode='green',name='gacha_r',glow=(90,160,255),gl=0.7),
 'C07':dict(src='v00',ss=2.00,to=4.60,mode='grab',name='gacha_sr'),
 'C08':dict(src='v01',ss=0.20,to=4.95,mode='none',name='gacha_ur_build',speed=1.55),
 'C09':dict(src='v02',ss=0.00,to=4.60,mode='none',name='gacha_ur_finale',speed=1.15),
 'C12':dict(src='v11',ss=0.50,to=3.50,mode='green',name='login_bonus'),
 'C13':dict(src='v12',ss=1.75,to=4.75,mode='green',name='set_complete'),
 'C14':dict(src='v13',ss=1.90,to=4.90,mode='grab',name='rank_up'),
 'C03':dict(src='w16',ss=1.60,to=4.40,mode='plain',name='gacha'),
 'C04':dict(src='w18',ss=0.30,to=3.70,mode='plain',name='victory'),
 'C10':dict(src='w17',ss=0.30,to=3.30,mode='plain',name='levelup'),
 'C11':dict(src='w19',ss=0.80,to=3.85,mode='plain',name='perfect'),
 'C16':dict(src='w20',ss=1.40,to=5.00,mode='plain',name='lose',speed=1.2),
 'C15':dict(src='v14',ss=2.45,to=5.00,mode='plain',name='streak'),
}
def run(cid):
    c=CLIPS[cid]; fr=read(c['src'])
    i0=int(round(c['ss']*24)); i1=min(int(round(c['to']*24)),len(fr)-1)
    sel=fr[i0:i1+1]; out=[]; prev=None; shp=None
    n=len(sel)
    for k,f in enumerate(sel):
        if c['mode']=='none': o=f.copy()
        elif c['mode']=='grab': o,prev=unify2(f,prev)
        elif c['mode']=='plain': o=unify(f)
        else:
            # green: key + temporally smoothed shadow + optional glow
            G,gs=greenmask(f)
            fgm=(~(cv2.morphologyEx(G.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))>0)).astype(np.uint8)
            near=cv2.dilate(1-fgm,np.ones((5,5),np.uint8))>0
            fgm[near&(gs>8)]=0
            nn,l2,st,_=cv2.connectedComponentsWithStats(fgm,connectivity=8)
            keep=st[:,cv2.CC_STAT_AREA]>=60; keep[0]=False; fgm=keep[l2].astype(np.uint8)
            a=cv2.GaussianBlur(fgm.astype(np.float32),(0,0),1.0); a=np.clip((a-0.15)/0.7,0,1)
            F=f.astype(np.float32); gmax=np.maximum(F[...,0],F[...,2]); sp=np.maximum(F[...,1]-gmax-4,0)
            F[...,1]-=sp; F[...,0]+=sp*0.3; F[...,2]+=sp*0.3
            ys,xs=np.where(a>0.6)
            p=np.array([np.percentile(ys,99.7),*np.percentile(xs,[3,97]),np.percentile(ys,2)])
            shp=p if shp is None else shp*0.7+p*0.3
            fy,x0,x1,top=shp
            bg=np.ones((S,S,3),np.float32)*CREAM
            if 'glow' in c:
                t=k/max(n-1,1); amp=c['gl']*np.clip(t/0.35,0,1)
                cx=(x0+x1)/2; cy=top+(fy-top)*0.35; r=(x1-x0)*0.9
                gg=np.exp(-(((xx*S-cx)**2+(yy*S-cy)**2)/(2*(r*0.6)**2)))*amp
                bg=bg*(1-gg[...,None])+np.array(c['glow'],np.float32)*gg[...,None]
            sh=shadow((x0+x1)/2,x1-x0,fy-4,0.16)
            bg=bg*(1-sh[...,None])+np.array([160,140,112],np.float32)*sh[...,None]
            o=np.clip(F*a[...,None]+bg*(1-a[...,None]),0,255).astype(np.uint8)
        out.append(o)
    out=np.stack(out)
    O=OUT
    for arr,suf in ((out,''),(sel,'_raw')):
        q=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{S}x{S}','-r','24','-i','-','-c:v','libx264','-qp','0','-preset','ultrafast','-pix_fmt','yuv444p',f'{O}/{cid}{suf}_master.mkv'],stdin=subprocess.PIPE); q.stdin.write(arr.tobytes()); q.stdin.close(); q.wait()
    sp=c.get('speed',1.0)
    mp4=f"{OUT}/{c['name']}.mp4"
    p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{S}x{S}','-r','24','-i','-',
        '-vf',f'setpts=PTS/{sp},fps=24','-c:v','libx264','-preset','slow','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart','-an',mp4],stdin=subprocess.PIPE)
    p.stdin.write(out.tobytes()); p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg','-y','-v','error','-i',mp4,'-frames:v','1','-c:v','libwebp','-quality','80',mp4.replace('.mp4','-poster.webp')])
    print(cid,mp4,os.path.getsize(mp4)//1024,'KB',round(len(out)/24/sp,2),'s')
if __name__=='__main__':
    for cid in sys.argv[1:]: run(cid)
