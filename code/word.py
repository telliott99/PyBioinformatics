class word:
    SZ = 32
    def __init__(self,n):
        if type(n) == type('a'):
            b = n.rjust(word.SZ,'0')
        elif type(n) == type(1):
            b = bin(n)[2:]
        else:
            raise ValueError, "can't do that"
        self.b = b.rjust(word.SZ,'0')
        
    def __repr__(self):
        b = self.b
        s = ' '.join([b[:8], b[8:16], b[16:24], b[24:]])
        s += ' = ' + str(eval('0b' + self.b))
        return s
        
    def __add__(self, a):
        carry = '0'
        rL = list()
        for i in range(len(self.b)-1,-1,-1):
            x = self.b[i]
            y = a.b[i]
            t = x+y
            if (t == '01' or t == '10'):
                if carry == '0':
                    rL.append('1')
                if carry == '1':
                    rL.append('0')
            elif t == '00':
                rL.append(carry)
                carry = '0'
            else:
                assert t == '11'
                if carry == '0':
                    rL.append('0')
                    carry = '1'
                else:
                    rL.append('1')
                    carry = '1'
        if carry == '1':
            raise ValueError, 'overflow'
        rL.reverse()
        return word(''.join(rL))
    
    def __mul__(self, a):
        L = list()
        for i in range(len(self.b)-1,-1,-1):
            x = self.b[i]
            if not x == '1':
                continue
            n = word.SZ - i - 1
            r = word(a.b[n:] + '0'*(n))
            L.append(r)
        res = L.pop(0)
        #print 'start:       ', res
        while L:
            next = L.pop(0)
            #print 'next:        ', next
            res = res + next
            #if L:
                #print 'intermediate:', 
            #else:
                #print 'result:      ',
            #print res
        return res

    def __pow__(self, n):
        res = self
        for i in range(n-1):
            res = res * self
        return res