#-*- encoding: utf-8 -*-

class A():
    #a = 1

    def test(self):
        print self.a

class B(A):
    a = 2
    
    def test2(self):
        self.test()

    

b = A()
#print b.a

c = B()
c.test()
c.test2()


t = True
print type(t)
print type(None)



import  base64

print base64.b64decode('LzIwMTEvMDMvMTcvNTMvNzY1N2IzZmY4NTQ5OGFiZmExMWY4OThjMzQ1OTg0NDUwcC0wMDAwLmZsdi5tM3U4P3A9aXBhZA==')


s = u'sss'
print type(s)
