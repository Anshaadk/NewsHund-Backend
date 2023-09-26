s='abcdp'
s=sorted(s)
r=[]
r.append(0)
j=''
m=0
k=0
ff=0
for i in s:
    ff=ff+1
    if i > j or j == '' :
        if k==1:  
            r.append(m)  
            print('one')
            m=0
            k=0
         
        j=i
        
        print(j,i)
        print(m)

    else:
        print('ss')
        m=m+1
        
        k=1
t=max(r)
print(r)
