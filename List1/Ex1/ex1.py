from matplotlib import pyplot as plt
from random import randint, choice
from fractions import gcd
from functools import reduce

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def make_random_generator(a, c, m):
    x = randint(0, m)
    while True:
        x = (a*x + c) % m
        yield x

def attack_modulus(sample):
    diffs = [x1 - x2 for x1, x2 in zip(sample, sample[1:])]
    zeros = [d2 * d0 - d1 * d1 for d0, d1, d2 in zip(diffs, diffs[1:], diffs[2:])]
    return abs(reduce(gcd, zeros))

def is_prime(n):
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  f = 5
  while f <= r:
    if n%f == 0: return False
    if n%(f+2) == 0: return False
    f +=6
  return True 

def attack_modulus_test():
    primes = [i for i in range(100000, 1000000) if is_prime(i)]
    ys = []
    probeNo = 1000
    for n in range(5, 100):
        counter = 0
        for _ in range(1, probeNo):
            m = choice(primes)
            a = randint(0, m)
            c = randint(0, m)

            generator = make_random_generator(a, c, m)
            sample = [next(generator) for _ in range(1, n)]
            if attack_modulus(sample) == m:
                counter += 1
        ys.append(counter / probeNo)

    plt.plot(range(5, 100), ys)
    plt.show()

def attack_a(x0, x1, x2, x3, modulus):
    a = 0
    try:
        return ((x2 - x1) * modinv(x1 - x0, modulus)) % modulus
    except Exception:
        try:
            return ((x3 - x2) * modinv(x2 - x1, modulus)) % modulus
        except Exception:
            return -1

def attack_a_test():
    m = randint(100000, 1000000)
    a = randint(0, m)
    c = randint(0, m)

    generator = make_random_generator(a, c, m)

    x0 = next(generator)
    x1 = next(generator)
    x2 = next(generator)
    x3 = next(generator)

    print(a, attack_a(x0, x1, x2, x3, m))

def attack_c(x0, x1, a, modulus):
    return (x1 - x0 * a) % modulus

def attack_generator(generator):
    sample = [next(generator) for _ in range(1, 16)]
    modulus = attack_modulus(sample)
    a = -1
    i = 0
    while a == -1 and i < 14 - 3:
        a = attack_a(sample[i], sample[i + 1], sample[i + 2], sample[i + 3], modulus)
        i += 1
    if a == -1:
        return "Error"
    c = attack_c(sample[0], sample[1], a, modulus)
    return (a, c, modulus)

# m = randint(100000, 1000000)
# a = randint(0, m)
# c = randint(0, m)

# generator = make_random_generator(a, c, m)

# print(attack_generator(generator))
# print(a, c, m)

attack_modulus_test()