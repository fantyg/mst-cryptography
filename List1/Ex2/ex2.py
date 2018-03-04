from numpy import random as rd
from collections import deque
from matplotlib import pyplot as plt

def glibc_random_generator(seed):
    states = deque([])
    states.append(seed)
    for _ in range(1, 31):
        i = len(states)
        states.append((16807 * states[i - 1]) % 2147483647)
    for _ in range(31, 34):
        states.append(states[-1])
    for _ in range(0, 311):
        i = len(states)
        newVal = (states[i - 3] + states[i - 31]) % 4294967296
        states.popleft()
        states.append(newVal)

    while True:
        i = len(states)
        newVal = (states[i - 3] + states[i - 31]) % 4294967296
        states.popleft()
        states.append(newVal)
        yield newVal >> 1

def probability_of_choice_in_attack():
    counter = [0, 0, 0]
    for _ in range(0, 10000):
        generator = glibc_random_generator(rd.randint(1, 2 ** 30))
        probe = deque([next(generator) for _ in range(0, 31)])
        for _ in range(0, 10000):
            guess1 = (probe[0] + probe[28]) % (2 ** 31)
            guess2 = (probe[0] + probe[28] + 1) % (2 ** 31)
            value = next(generator)
            probe.popleft()
            if guess1 == value:
                counter[0] += 1
            elif guess2 == value:
                counter[1] += 1
            else:
                counter[2] += 1
            probe.append(value)

    print(counter)
    counter = [c / sum(counter) for c in counter]
    print(counter)
    
def attack_glib(generator):
    probe = deque([next(generator) for _ in range(0, 31)])
    for _ in range(0, 10000):
            guess = (probe[0] + probe[28]) % (2 ** 31)
            value = next(generator)
            yield (guess, value)
            probe.popleft()
            probe.append(value)

counter = [0 for _ in range(1, 2 ** 7)]
for i, seed in enumerate(range(1, 2 ** 7)):
    generator = glibc_random_generator(seed)
    attack = attack_glib(generator)
    
    for _ in range(0, 10000):
        guessing = next(attack)
        if guessing[0] == guessing[1]:
            counter[i] += 1
    counter[i] /= 10000

plt.plot(range(1, 2 ** 7), counter)
plt.show()