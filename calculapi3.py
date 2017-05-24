import functools, random



def sample(p):
    x, y = random.random(),random.random()
    return 1 if x*x + y*y < 1 else 0

def calcula_pi(p):
    return 4.0*(functools.reduce(lambda a, b: a + b, map(sample,range(0, p))))/p

print (calcula_pi(3000))