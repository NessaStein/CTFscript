#!/usr/bin/env python
# -- coding:utf-8 --
# Author:	xuanxuan
# Date:		2019-09-25

import re

frequencies = {
"e": 0.12702, "t": 0.09056, "a": 0.08167, "o": 0.07507, "i": 0.06966,
"n": 0.06749, "s": 0.06327, "h": 0.06094, "r": 0.05987, "d": 0.04253,
"l": 0.04025, "c": 0.02782, "u": 0.02758, "m": 0.02406, "w": 0.02360,
"f": 0.02228, "g": 0.02015, "y": 0.01974, "p": 0.01929, "b": 0.01492,
"v": 0.00978, "k": 0.00772, "j": 0.00153, "x": 0.00150, "q": 0.00095,
"z": 0.00074
}

def Shift_crack(cipher):
	b,s = [],[]
	cipher = cipher.lower()
	a = re.sub("[^a-zA-Z ]","",cipher)
	lenth = len(a.replace(" ",""))
	for j in range(26):
		c = ""
		for i in a:
			if i!=" ":
				c+=chr((((ord(i)-97)+j)%26)+97)
			else:
				c+=i
		b.append(c)
	for j in b:
		d = {}
		sum = 0
		for i in j:
			if i!=" ":
				d[i]=j.count(i)/float(lenth)
		for i in d:
			sum+=d[i]*frequencies[i]
		s.append(abs(sum-0.065))
	key = 26-s.index(min(s))
	message = b[s.index(min(s))]
	return key,message

def guesskeylenth(cipher,keylenth):
	cipher = cipher.lower()
	cipher = re.sub("[^a-zA-Z ]","",cipher)
	estimatelist = []
	for i in range(keylenth):
		i += 1
		tablelength = i 
		m = []
		for j in range(i):
			mm = ""
			for k in range(len(cipher)/i):
				try:
					mm += cipher[j+i*k]
				except:
					break
			m.append(mm)
		#print "---------"
		sumlist = []
		for c in m:
			result = {}
			for i in c:
				result[i] = (c.count(i))/float(len(c))
			#print result
			sum = 0
			for i in result:
				sum += result[i]*result[i]
			sumlist.append(sum)
		print "[+] 猜测密码长度为: "+str(tablelength)+" 时的概率表"
		print sumlist
		print ""
		estimate = 0
		for i in sumlist:
			estimate += (i-0.065)*(i-0.065)
		estimate /= len(sumlist)
		estimatelist.append(estimate)
	tmp = []
	for i in estimatelist:
		tmp.append(i)
	#print estimatelist
	r1 = estimatelist.index(min(tmp))+1
	tmp.remove(min(tmp))
	r2 = estimatelist.index(min(tmp))+1
	tmp.remove(min(tmp))
	r3 = estimatelist.index(min(tmp))+1
	tmp.remove(min(tmp))

	print "[+] 概率接近0.065的密码长度:"
	print r1,r2,r3
	return r1,r2,r3

def divide(cipher,lenth):
	cipher = cipher.lower()
	cipher = re.sub("[^a-zA-Z ]","",cipher)
	cipher = cipher+'a'*(lenth-len(cipher)%lenth)
	m = []
	for j in range(lenth):
		mm = ""
		for k in range(len(cipher)/lenth):
			mm += cipher[j+lenth*k]
		m.append(mm)
	return m

def Vigenere_crack(cipher,keymaxlength=10):
	maylenth =  guesskeylenth(cipher,keymaxlength)
	returnvalue = {}
	print "--------------------------- 解密 ---------------------------"
	for may in maylenth:
		s = divide(cipher,may)
		key = ""
		message = []
		me = ""
		print "[+] 当密码长度为："+str(may)
		for i in s :
			k,m = Shift_crack(i)
			key += chr(k%26+97)
			message.append(m)
		for i in range(len(message[0])):
			for j in range(may):
				me += message[j][i]
		returnvalue[key] = me
		print "[+] 密码为: " + key
		print "[+] 明文为: " + me
		print ""
	return returnvalue


def Vigenere_force(cipher,keymaxlength=10):
	maylenth = range(keymaxlength)
	returnvalue = {}
	print "--------------------------- 爆破 ---------------------------"
	for may in maylenth:
		may += 1
		s = divide(cipher,may)
		key = ""
		message = []
		me = ""
		print "[+] 当密码长度为："+str(may)
		for i in s :
			k,m = Shift_crack(i)
			key += chr(k%26+97)
			message.append(m)
		for i in range(len(message[0])):
			for j in range(may):
				me += message[j][i]
		returnvalue[key] = me
		print "[+] 密码为: " + key
		print "[+] 明文为: " + me
		print ""
	return returnvalue

if __name__ == '__main__':

	vigenere_cipher = """
	xvsgoucgqbeffymrkmiaaosgocayzingoilfvmtrjmaezbigbwthoycbkmifqmospcmnqccfmfc
	ftbipewozjonvzutrtctuxninbhgvkyeefhgfqutvlhaaamcnauhzfinbkysvayaaawoaqloyfh
	dhpnrvxfslpnezpingeyogeyrffxegeynrtyriblsvlhsbcnhrxlcufnepqorrxlepiuizbxtby
	ysrzorrxaavkmtfljhvpnipxneqxntnzeeepmiazytubsufbudixhcrawrlmnotoupufwpefgig
	fpefxhdcoitbzilffhtufmpnmyrjbmhbtnhnqyvrknhriutrpnvromibkmosqbeqbpipbmaaajr
	bqicbimaebmtvifvhiheexvlrxztroleiblsrbhgvkyeefhggeycevjtbdlacecccoitbziljbu
	rrxvlrqicebutrxlotryeadcnrbliadmtnqcoatbipewaajusdryrnayafqbegfutbqbeciwaaa
	cnwbwtnksmrpmatbmfnsiuexvlrqitubutgxwkrousnccrfqyxnjjlrtyekqynqxntnzesgeutp
	xhrrjitrissgxltbomtbmnhrmfcglnhriutrpnsciwsbrlmnfhagqucxzunqlqnyludplhtelfl
	bdccbcnhrxntnzeeepwhbfweglurrjitrmfcbrlsgointbmtnqnaphnhrpneninhcoigexgiagy
	cgfinnqnaphwaapypnoutrismbacflqbeerhnvkacbayaaanhrpiuezycbaywufwhnoybbqbdbt
	hlbxxeqqitubjlpqbifxflbtmufqimbacflqbeplhtelflbdccbcnhrmfcjeclroytnfhiadnhr
	piuezycbaytubjlpmlefbhtfqitubyntfherocntpnagfingeosjbwaazlenqyaffnunqcoatbe
	ebnhrmfcfconpqcoaxfigvcsqfzfroyngclozqbeplhtelflbdccifmioiytbqberkaiabyr
	"""
	shift_cipher="""
	lmdeclne. dtpxpyd tyofdectlw nzyeczw djdepx lcnstepnefcp td nzxazdpo zq dtxl
	etn d7 aczrclxxlmwp wzrtn nzyeczwwpc (awn). esp qzcxpc nzxxfytnlepd htes etl 
	pyrtyppctyr deletzy lyo dnlol xly-xlnstyp tyepcqlnp, hstwp esp wleepc nzyecz
	wd tyofdectlw djdepx. wlepc gpcdtzyd zq esp lcnstepnefcp nwltx ez mp lmwp ez 
	htesdelyo nzxawpi leelnvpcd mpnlfdp espj fdp loglynpo pyncjaetzy actxtetgpd 
	lyo aczeznzwd. ty estd lcetnwp, hp dszh esle pgpy esp wlepde gpcdtzyd zq opg
	tnpd lyo aczeznzwd lcp detww qclrtwp. lqepc cpgpcdp-pyrtyppctyr esp ncjaezrc
	lastn aczeznzw, hp nly ncplep l czrfp pyrtyppctyr deletzy esle nly otdrftdp 
	etl ez awn lyo tyupne lyj xpddlrp mpypqtntlw ez esp leelnvpc. ld esp qtcde p
	ilxawp, hp htww piepyo esp leelnv esle nly delce zc deza esp aczrclxxlmwp wz
	rtn nzyeczwwpc cpxzepwj ez esp wlepde d7-1500 aczrclxxlmwp wzrtn nzyeczwwpc. 
	zfc xlty leelnv nly ozhywzlo esp nzyeczw wzrtn nszdpy mj esp leelnvpc ez l c
	pxzep awn. zfc deczyrpde leelnv, esp deplwes aczrclx tyupnetzy leelnv, nly x
	zotqj esp cfyytyr nzop lyo esp dzfcnp nzop dpalclepwj, mzes zq hstns lcp ozh
	ywzlopo ez esp aczrclxxlmwp wzrtn nzyeczwwpc. estd lwwzhd fd ez xzotqj esp n
	zyeczw wzrtn zq esp aczrclxxlmwp wzrtn nzyeczwwpc hstwp cpeltytyr esp dzfcnp 
	nzop esle esp aczrclxxlmwp wzrtn nzyeczwwpc acpdpyed ez esp pyrtyppctyr dele
	tzy. espcpqzcp, hp nly ncplep l dtefletzy hspcp esp qfynetzy zq awn td otqqp
	cpye qczx esp nzyeczw wzrtn gtdtmwp ez pyrtyppcd.
	"""

	Vigenere_force(vigenere_cipher)
	Vigenere_crack(vigenere_cipher)
	Vigenere_crack(shift_cipher)