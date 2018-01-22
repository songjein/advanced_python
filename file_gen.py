f = open("wise.txt")
f0 = open("0.txt","w")
f1 = open("1.txt","w")
f2 = open("2.txt","w")
f3 = open("3.txt","w")


c = 0
for l in f:
	if c < 5000:
		f0.write("{}".format(l))
	elif c < 10000:
		f1.write("{}".format(l))
	elif c < 15000:
		f2.write("{}".format(l))
	elif c < 20000:
		f3.write("{}".format(l))
	c += 1
'''
for i in range(1000000):
	a = ("aaaaa{}\n".format(i))
	b = ("bbbbb{}\n".format(i))
	c = ("ccccc{}\n".format(i))
	d = ("ddddd{}\n".format(i))
	f0.write(a)
	f1.write(b)
	f2.write(c)
	f3.write(d)
	f.write(a)
	f.write(b)
	f.write(c)
	f.write(d)
	'''
