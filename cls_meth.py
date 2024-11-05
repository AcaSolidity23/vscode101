class A():
    count = 0
    def __init__(self):
        A.count +=1
    def exclaim(self):
        print('I am an A!')
    @classmethod
    def kids(cls):
        print('A has', cls.count, 'little objects.')
        
easy_a = A()
easy_b = A()
wheezy_a = A()
A.kids()

