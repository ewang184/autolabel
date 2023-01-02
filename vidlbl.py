import numpy as np
import cv2 as cv
import pathlib
import os

#there should be 2 prevs

def topy(npa,prev,x1,x2):
	l = len(npa[0])
	for i in range(len(npa)-prev):
		if( not np.array_equal(npa[i-1+prev][x1:l-x2], np.zeros((npa[i][x1:l-x2]).shape)) ):
			return i+prev
		#else:
		#	print((npa[i-1+prev][x1:l-x2]).shape)
		#	print((npa[i][x1:l-x2]).shape)
			
	return -1
	#for i in range(prev, len(npa)):
	#	for j in range(x1, len(npa[0])-x2):
	#		if(npa[i,j] != 0):
	#			return i
	#return -1

def boty(npa,prev,x1,x2):
	l = len(npa[0])
	for i in range(len(npa)-prev):
		if( not np.array_equal(npa[len(npa)-prev-i-1][x1:l-x2], np.zeros((npa[i][x1:l-x2]).shape)) ):
			return (prev+i)
	return -1
	#for i in range(0, len(npa)-prev):
	#	for j in range(x1, len(npa[0])-x2):
	#		if(npa[i,j] != 0):
	#			return i
	#return -1
def lefx(npa,prev,y1,y2):
	npa = npa.T
	l = len(npa[0])
	for i in range(len(npa)-prev):
		if( not np.array_equal(npa[i-1+prev][y1:l-y2], np.zeros((npa[i][y1:l-y2]).shape)) ):
			return i+prev
	return -1
	#for i in range(prev, len(npa)):
	#	for j in range(y1, len(npa[0])-y2):
	#		if(npa[i,j] != 0):
	#			return i
	#return -1

def rigx(npa,prev,y1,y2):
	npa = npa.T
	l = len(npa[0])
	for i in range(len(npa)-prev):
		if( not np.array_equal(npa[len(npa)-prev-i-1][y1:-y2], np.zeros((npa[i][y1:l-y2]).shape)) ):
			return (prev+i)
	return -1
	#for i in range(0, len(npa)-prev):
	#	for j in range(y1, len(npa[0])-y2):
	#		if(npa[i,j] != 0):
	#			return i
	#return -1

def drawVert(x, npa):
	for i in range(len(npa)):
		npa[i][x] =255
	return npa

def drawHrzn(x, npa):
	for i in range(len(npa[0])):
		npa[x][i] =255
	return npa

def drawVertB(x, npa):
	for i in range(len(npa)):
		npa[i][x] =0
	return npa

def drawHrznB(x, npa):
	for i in range(len(npa[0])):
		npa[x][i] =0
	return npa

def createlabel(lblname, text, type):
	targetdir = os.path.join(curpath, f'{type}\labels')
	targetdir = os.path.join(targetdir,lblname)
	file = open(targetdir,"a")
	text = text+"\n"
	file.write(text)

def createimg(imgname, npa, type):
	targetdir = os.path.join(curpath, f'{type}\images')
	targetdir = os.path.join(targetdir,imgname)
	cv.imwrite(targetdir, npa)

#________________________start program

curpath = pathlib.Path(__file__).parent.absolute()

imgpath = os.path.join(curpath,"testblue.png")

img=cv.imread(imgpath)

img2 = cv.GaussianBlur(img,(15,15),0)

img3 = cv.bilateralFilter(img,15,80,80)

hsv = cv.cvtColor(img3,cv.COLOR_BGR2HSV)

lower_blue = np.array([100,80,160])
upper_blue = np.array([104,255,240])

#get data directories



vidpath = os.path.join(curpath,"onlyorange.mp4")

cap = cv.VideoCapture(vidpath)

lower_orange = np.array([12,80,160])
upper_orange = np.array([45,255,220])

lower_blue = np.array([98,80,160])
upper_blue = np.array([102,255,220])


la=0
lb=0
lc=300
ld=300

bla=0
blb=0
blc=300
bld=300

counter = 0
secondcounter = 0

while cap.isOpened():

	ret,frame = cap.read()
	
	if not ret:
		print("cant receive frame exiting")
		break
	img3 = cv.bilateralFilter(frame,15,80,80)
	hsv = cv.cvtColor(img3,cv.COLOR_BGR2HSV)
	orange = cv.inRange(hsv,lower_orange,upper_orange)
	blue = cv.inRange(hsv,lower_blue,upper_blue)

	
#_____________________________________________________________
	a=topy(orange,0,lc,ld)
	b=boty(orange,0,lc,ld)
	c=lefx(orange,0,la,lb)
	d=rigx(orange,0,la,lb) 
	if(la != -1 or lb != -1 or lc != -1 or ld != -1):
		while(abs(a-la)>30 and a > 0):
			preva=a
			a = topy(orange,preva+1,lc,ld)

		while(abs(b-lb)>30 and b>0):
			prevb=b
			b = boty(orange,prevb+1,lc,ld)

		while(abs(c-lc)>30 and c > 0):
			prevc=c
			c = lefx(orange,prevc+1,la,lb)

		while(abs(d-ld)>30 and d>0):
			prevd=d
			d = rigx(orange,prevd+1,la,lb)

	ISCIRCLE = (not (a==-1 and b==-1 and c==-1 and d==-1))

	if(la==a or (a==-1 and ISCIRCLE)):
		la+=5
	elif((not ISCIRCLE) and la>5):
		la-=5
	elif(a > 0):
		la=a

	if(lb==b or (b==-1 and ISCIRCLE)):
		lb+=5
	elif((not ISCIRCLE) and lb>5):
		lb-=5
	elif(b > 0):
		lb=b

	if(lc==c or (c==-1 and ISCIRCLE)):
		lc+=5
	elif((not ISCIRCLE) and lc>205):
		lc-=5
	elif(c > 0):
		lc=c
	if(ld==d or (d==-1 and ISCIRCLE)):
		ld+=5
	elif((not ISCIRCLE) and ld>205):
		ld-=5
	elif(d > 0):
		ld=d

	#print(f"last[{la},{lb},{lc},{ld}]")
	#print(f"abcd[{a},{b},{c},{d}]")
	orange = drawVert(lc,orange)
	orange = drawVert(1278-ld,orange)
	orange = drawHrzn(la,orange)
	orange = drawHrzn(718-lb,orange)

	#frame = drawVertB(lc,frame)
	#frame = drawVertB(1278-ld,frame)
	#frame = drawHrznB(la,frame)
	#frame = drawHrznB(718-lb,frame)
	
	cv.imshow("orange", orange)
#_____________________________________________________
	ba=topy(blue,0,blc,bld)
	bb=boty(blue,0,blc,bld)
	bc=lefx(blue,0,bla,blb)
	bd=rigx(blue,0,bla,blb) 
	if(bla != -1 or blb != -1 or blc != -1 or bld != -1):
		while(abs(ba-bla)>30 and ba > 0):
			preva=ba
			ba = topy(blue,preva+1,blc,bld)

		while(abs(bb-blb)>30 and bb>0):
			prevb=bb
			bb = boty(blue,prevb+1,blc,bld)

		while(abs(bc-blc)>30 and bc > 0):
			prevc=bc
			bc = lefx(blue,prevc+1,bla,blb)

		while(abs(bd-bld)>30 and bd>0):
			prevd=bd
			bd = rigx(blue,prevd+1,bla,blb)

	BISCIRCLE = (not (ba==-1 and bb==-1 and bc==-1 and bd==-1))

	if(bla==ba or (ba==-1 and BISCIRCLE)):
		bla+=20
	elif((not BISCIRCLE) and (bla-5)>0):
		bla-=5
	elif(ba > 0):
		bla=ba

	if(blb==bb or (bb==-1 and BISCIRCLE)):
		blb+=20
	elif((not BISCIRCLE) and (blb-5)>0):
		blb-=5
	elif(bb > 0):
		blb=bb

	if(blc==bc or (bc==-1 and BISCIRCLE)):
		blc+=20
	elif((not BISCIRCLE) and (blc-5)>200):
		blc-=5
	elif(bc > 0):
		blc=bc

	if(bld==bd or (bd==-1 and BISCIRCLE)):
		bld+=20
	elif((not BISCIRCLE) and (bld-5)>200):
		bld-=5
	elif(bd > 0):
		bld=bd

	#print(f"last[{bla},{blb},{blc},{bld}]")
	#print(f"abcd[{ba},{bb},{bc},{bd}]")
	blue = drawVert(blc,blue)
	blue = drawVert(1278-bld,blue)
	blue = drawHrzn(bla,blue)
	blue = drawHrzn(718-blb,blue)
	cv.imshow("blue", blue)

#______________________________________________________

	cv.imshow("video", frame)

#______________________________________________________
#orange is 183, blue is 184
	ox = ((1280-ld-lc)/2+lc) * 1/1280
	oy = ((720-lb-la)/2+la) * 1/720
	oh = (720-lb-la) * 1/720
	ow = (1280-ld-lc) * 1/1280

	bx = ((1280-bld-blc)/2+blc) * 1/1280
	by = ((720-blb-bla)/2+bla) * 1/720
	bw = (1280-bld-blc) * 1/1280
	bh = (720-blb-bla) * 1/720

	#texto = "183" +" "+ str(ox) +" "+ str(oy) +" "+ str(ow) +" "+ str(oh)
	#textb = "184" +" "+ str(bx) +" "+ str(by) +" "+ str(bw) +" "+ str(bh)
	#print(texto)

	if(True):
		if(counter % 10 == 0):
			if(a != -1 and b != -1 and c != -1 and d != -1):
				createlabel(f"{counter}orange.txt", texto, "test")
				createimg(f"{counter}orange.jpg", frame, "test")
				
			if(ba != -1 and bb != -1 and bc != -1 and bd != -1):
				createlabel(f"{counter}blue.txt", textb, "test")
				createimg(f"{counter}blue.jpg", frame, "test")
		else:
			if(a != -1 and b != -1 and c != -1 and d != -1):
				createlabel(f"{counter}orange.txt", texto, "train")
				createimg(f"{counter}orange.jpg", frame, "train")
	
			if(ba != -1 and bb != -1 and bc != -1 and bd != -1):
				createlabel(f"{counter}blue.txt", textb, "train")
				createimg(f"{counter}blue.jpg", frame, "train")
	
		counter +=1
	secondcounter +=1

	if cv.waitKey(1) == ord("q"):
		break
cap.release
cv.destroyAllWindows()
