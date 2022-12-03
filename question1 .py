#Simple calculator using python

class Calculator:
    def add(a,b):
        return a+b

    def sub(a,b):
        return a-b

    def mul(a,b):
        return a*b

    def div(a,b):
        return a/b
    
print('Options:')
print('1.Addition')
print('2.Subtraction')
print('3.Multiplication')
print('4.Division')

while True:
    select = int(input('Select from the option :'))
    a = int(input('Enter the no.:'))
    b = int(input('Enter the no.:'))

    
    if select == 1:
        print(a,'+',b,'=',Calculator.add(a,b))

    elif select == 2:
         print(a,'-',b,'=',Calculator.sub(a,b))

    elif select == 3:
        print(a,'*',b,'=',Calculator.mul(a,b))

    elif select == 4:
        print(a,'/',b,'=',Calculator.div(a,b))


    else:
        print("enter valid input")
        break



    



