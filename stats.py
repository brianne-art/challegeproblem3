import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# --- Build transition matrix ---
names_file = 'makemore/names.txt'
with open(names_file) as f:
    names = [line.strip().lower() for line in f if line.strip()]

# All unique chars + '.' sentinel
chars = ['.'] + sorted(set(c for name in names for c in name))
ctoi = {c: i for i, c in enumerate(chars)}
n = len(chars)

# Count transitions
counts = np.zeros((n, n), dtype=int)
for name in names:
    padded = '.' + name + '.'
    for a, b in zip(padded, padded[1:]):
        counts[ctoi[a]][ctoi[b]] += 1

# Probability matrix (row-normalized)
probs = counts.astype(float)
row_sums = probs.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1  # avoid div-by-zero
probs /= row_sums

# --- Heatmap ---
fig, ax = plt.subplots(figsize=(18, 16))
im = ax.imshow(probs, cmap='Blues', aspect='auto')
plt.colorbar(im, ax=ax, label='Probability')

ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(chars, fontsize=8)
ax.set_yticklabels(chars, fontsize=8)
ax.set_xlabel('Second letter', fontsize=12)
ax.set_ylabel('First letter', fontsize=12)
ax.set_title('Bigram Transition Probabilities — real names', fontsize=14)

# Annotate cells with counts (only where count > 0, skip tiny values for clarity)
for i in range(n):
    for j in range(n):
        if counts[i][j] > 0:
            ax.text(j, i, str(counts[i][j]),
                    ha='center', va='center', fontsize=4,
                    color='white' if probs[i][j] > 0.4 else 'black')

plt.tight_layout()
plt.savefig('heatmap_real.png', dpi=150)
print("Saved heatmap_real.png")

# --- Answer the questions ---
dot_idx = ctoi['.']

# Starting letters: row for '.' (prob of each letter following '.')
start_probs = probs[dot_idx]
# Exclude '.' itself
letter_start = [(chars[i], start_probs[i]) for i in range(n) if chars[i] != '.']
letter_start.sort(key=lambda x: -x[1])
print("\nTop 3 most likely starting letters:")
for ch, p in letter_start[:3]:
    print(f"  {ch}: {p:.4f}")
print("Top 3 least likely starting letters (non-zero):")
nonzero_start = [(ch, p) for ch, p in letter_start if p > 0]
for ch, p in nonzero_start[-3:]:
    print(f"  {ch}: {p:.4f}")

# Ending letters: column for '.' (prob of '.' following each letter)
end_probs = probs[:, dot_idx]
letter_end = [(chars[i], end_probs[i]) for i in range(n) if chars[i] != '.']
letter_end.sort(key=lambda x: -x[1])
print("\nTop 3 most likely ending letters:")
for ch, p in letter_end[:3]:
    print(f"  {ch}: {p:.4f}")
print("Top 3 least likely ending letters (non-zero):")
nonzero_end = [(ch, p) for ch, p in letter_end if p > 0]
for ch, p in nonzero_end[-3:]:
    print(f"  {ch}: {p:.4f}")

# Letters following 'q'
q_idx = ctoi.get('q')
if q_idx is not None:
    q_row = counts[q_idx]
    print("\nLetters following 'q':")
    for i, c in enumerate(chars):
        if q_row[i] > 0:
            print(f"  '{c}': {q_row[i]} times")
else:
    print("\n'q' not in alphabet")

# Most likely second letter for names starting with 'x'
x_idx = ctoi.get('x')
if x_idx is not None:
    # Names starting with 'x': row in transition matrix for '.' is the first letter prob,
    # but we need the second letter given first='x'
    x_row = probs[x_idx]
    x_letters = [(chars[i], x_row[i]) for i in range(n) if chars[i] != '.']
    x_letters.sort(key=lambda x: -x[1])
    print(f"\nMost likely second letter for names starting with 'x': '{x_letters[0][0]}' ({x_letters[0][1]:.4f})")
    print("Full distribution for 'x':")
    for ch, p in x_letters:
        if p > 0:
            print(f"  x -> {ch}: {p:.4f} (count={counts[x_idx][ctoi[ch]]})")
