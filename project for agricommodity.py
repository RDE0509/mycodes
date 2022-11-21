
print("$"*3,'-'*3,'welcome to the commodity bazaar','$'*3,"-"*3)

#for selection of commodity

name = input('enter the name of commodity :')

l = ['wheat','soyabean','dollar', 'mirchi']
for i in l:
    if name== i:
     print('The Commodity you selected',i)
     break
else:
    print('commodity is not present')

# to check the available brand and selection of the brand


dict ={'wheat':['lok1','wh047'],

'soyabean':['soy12','mspl'],

'dollar':['d1m','dl12'],

'mirchi':['12','kolhapuri','kashmiri']

}



l =[]
x = input('enter your  commodity : \n ')
for key,value in dict.items():
     if x == key:
        print ('WE HAVE THAT brand IN YOUR COMMODITY :' ,value)
        for j in value:
            l.append(j)
        break
else:
        print('Brand is not available')

y = input('enter brand name : \n ')
if y in l:
        print('Brand is selected wait for the billing>>>>')
else:
       print('Brand is not availiable')




# for pricing of  the commodity

dict1 ={'lok1':3000,'wh047':4000,'soy12':9000,'mspl':10000,'d1m':7000,'lok1':3000,
'lok1':3000,'lok1':3000,'lok1':3000,'lok1':3000
}

for qual,pr in dict1.items():
    if y in dict1.keys():
        print(pr)








    
       






