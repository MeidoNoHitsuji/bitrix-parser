def test(a):
    a += ['123']
    
b = []
test(b)
print(b)

b.remove('123')

print(b)