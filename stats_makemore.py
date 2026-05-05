"""
Phase 4: Repeat the heatmap analysis on names produced by makemore,
then compare to the real-names heatmap.
Usage: python3 stats_makemore.py generated_names.txt
"""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) < 2:
    print("Usage: python3 stats_makemore.py <generated_names_file>")
    sys.exit(1)

gen_file = sys.argv[1]
with open(gen_file) as f:
    names = [line.strip().lower() for line in f if line.strip()]

print(f"Loaded {len(names)} generated names from {gen_file}")

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

fig, ax = plt.subplots(figsize=(18, 16))
im = ax.imshow(probs, cmap='Blues', aspect='auto')
plt.colorbar(im, ax=ax, label='Probability')
ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(chars, fontsize=8)
ax.set_yticklabels(chars, fontsize=8)
ax.set_xlabel('Second letter', fontsize=12)
ax.set_ylabel('First letter', fontsize=12)
ax.set_title('Bigram Transition Probabilities — makemore generated names', fontsize=14)
for i in range(n):
    for j in range(n):
        if counts[i][j] > 0:
            ax.text(j, i, str(counts[i][j]),
                    ha='center', va='center', fontsize=6,
                    color='white' if probs[i][j] > 0.4 else 'black')
plt.tight_layout()
plt.savefig('heatmap_makemore.png', dpi=150)
print("Saved heatmap_makemore.png")

dot_idx = ctoi['.']
start_probs = probs[dot_idx]
letter_start = [(chars[i], start_probs[i]) for i in range(n) if chars[i] != '.']
letter_start.sort(key=lambda x: -x[1])
print("\nTop 3 starting letters in makemore names:")
for ch, p in letter_start[:3]:
    print(f"  {ch}: {p:.4f}")

end_probs = probs[:, dot_idx]
letter_end = [(chars[i], end_probs[i]) for i in range(n) if chars[i] != '.']
letter_end.sort(key=lambda x: -x[1])
print("\nTop 3 ending letters in makemore names:")
for ch, p in letter_end[:3]:
    print(f"  {ch}: {p:.4f}")
