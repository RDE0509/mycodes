class Hotel:
    idlii=10
    dosai=15
    rotti=20
    pongl=30
    def __init__(self,idlyn=0,dosan=0,rottin=0,pongaln=0):
        self.idlyn=idlyn
        self.dosan=dosan
        self.rottin=rottin
        self.pongaln=pongaln
    def billing(self):
        d={}
        l=[self.idlyn*Hotel.idlii,self.dosan*Hotel.dosai,self.rottin*Hotel.rotti,self.pongaln*Hotel.pongl]
        l1=[['idlii','dosai','rotti','pongl'],[self.idlyn,self.dosan,self.rottin,self.pongaln]]
        count=0
        for i in l:
            if i!=0:
                d[l1[0][count]]=[l1[1][count],l[count]]
                count+=1
            else:
                count+=1
        print(''*2 + 'Shree Hotel' + ''*2)
        print('_'*15)
        print('item' + '|' +' Qty'+ '|' + ' ' +'Cost')
        print('_' * 15)
        for item in d.items():
            print(str(item[0])+'  '+str(item[1][0])+'  '+'='+' '+str(item[1][1]))
        print('_' * 15)
        print('    '+'Total'+' = '+str(sum(l)))
        print('' * 3+'thankyou'+'' * 3)
    @classmethod
    def menu(cls):
        l2=['idlii','dosai','rotti','pongl']
        l3=[Hotel.idlii,Hotel.dosai,Hotel.rotti,Hotel.pongl]
        men = {}
        digit = 0
        for food in l2:
            men[food] = l3[digit]
            digit += 1
        print('' * 5 + "welcome" + '' * 5)
        print('' * 6 + 'Menu' + '' * 6)
        print('-' * 15)
        print(' item ' + '|' + ' Cost ')
        print('-' * 15)
        for menus in men.items():
            print(menus[0] + ' |  ' + str(menus[1]))
        print('_' * 15)




Hotel.menu()
idly=0
dosa=0
roti=0
pongal=0
ins=1
while ins!=0:
    menu=input('Enter Dish name=')
    qty=int(input('Qty='))
    if menu=='idlii':
        idly=qty
    if menu=='dosai':
        dosa=qty
    if menu=='rotti':
        roti=qty
    if menu=='pongl':
        pongal=qty
    ins=int(input("Enter '0' got closing the order '1' for add item:"))
e1=Hotel(idlyn=idly,dosan=dosa,rottin=roti,pongaln=pongal)
e1.billing()
