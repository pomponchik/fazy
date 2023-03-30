import f


x = [1, 2, 3]
print(f('kek {x[1]} lol {x[0] + x[2]}'))
print(f('{"kek"}') == 'kek')
print('kek' == f('{"kek"}'))
print(repr(f('{"kek"}')))
print(f('{"kek"}').kek)
