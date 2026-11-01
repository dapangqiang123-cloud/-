exec(open(__file__.replace('fix_chair.py','prepare.py')).read().split("for k in")[0])
im=Image.open(R/'素材/chair.png').convert('RGB');small=im.resize((1600,1600));ar=np.array(small);mi=ar.min(2);ma=ar.max(2);spread=ma.astype(int)-mi.astype(int)
mask=np.full((1600,1600),cv2.GC_PR_BGD,dtype=np.uint8)
mask[(mi<240)&(spread>7)]=cv2.GC_PR_FGD
mask[(mi<210)&(spread>10)]=cv2.GC_FGD
mask[(mi>246)&(spread<8)]=cv2.GC_BGD
mask[:375,:]=cv2.GC_BGD;mask[1450:,:]=cv2.GC_BGD;mask[:,:165]=cv2.GC_BGD;mask[:,1450:]=cv2.GC_BGD
cv2.grabCut(ar,mask,None,np.zeros((1,65)),np.zeros((1,65)),4,cv2.GC_INIT_WITH_MASK)
a=np.where((mask==1)|(mask==3),255,0).astype('uint8');a=Image.fromarray(a).resize(im.size,Image.Resampling.LANCZOS)

# Remove only the photographed floor shadow below the furniture's true lower contour.
pts=[(0,0),(700,0),(700,580),(610,589),(590,597),(560,607),(520,615),(480,619),(455,614),(410,605),(382,596),(370,580),(365,551),(350,559),(320,568),(270,574),(220,573),(175,565),(155,555),(135,545),(0,530)]
p=Image.new('L',im.size);ImageDraw.Draw(p).polygon([(int(x*im.width/700),int(y*im.height/700)) for x,y in pts],fill=255);a=Image.fromarray(np.minimum(np.array(a),np.array(p)))
out=im.convert('RGBA');out.putalpha(a);out=out.crop(out.getbbox());out.save(A/'chair.png');out.thumbnail((900,700));bg=Image.new('RGBA',out.size,'#F0ECE1');bg.alpha_composite(out);bg.convert('RGB').save('/tmp/tresor-chair-cutout-v2.jpg');print('chair',out.size)
