import numpy as np

names_file = 'makemore/names.txt'
with open(names_file) as f:
    names = [line.strip().lower() for line in f if line.strip()]

chars = ['.'] + sorted(set(c for name in names for c in name))
ctoi = {c: i for i, c in enumerate(chars)}
n = len(chars)

counts = np.zeros((n, n), dtype=int)
for name in names:
    padded = '.' + name + '.'
    for a, b in zip(padded, padded[1:]):
        counts[ctoi[a]][ctoi[b]] += 1

probs = counts.astype(float)
row_sums = probs.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1
probs /= row_sums

rng = np.random.default_rng(42)

def random_choice(distribution):
    return rng.choice(len(distribution), p=distribution)

generated = []
while len(generated) < 25:
    letter_idx = ctoi['.']
    name = ''
    for _ in range(50):  # max length guard
        letter_idx = random_choice(probs[letter_idx])
        letter = chars[letter_idx]
        if letter == '.':
            break
        name += letter
    if len(name) >= 3:
        generated.append(name)

print("Generated names:")
for i, name in enumerate(generated, 1):
    print(f"  {i:2d}. {name}")
