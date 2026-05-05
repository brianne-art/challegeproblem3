# Project Questions

## 1. Three most and least likely starting letters

Most likely starting letters (from the '.' row of the transition matrix):
- **a**: 13.77%
- **k**: 9.25%
- **m**: 7.92%

Least likely starting letters (non-zero):
- **x**: 0.42%
- **q**: 0.29%
- **u**: 0.24%

## 2. Three most and least likely ending letters

Most likely ending letters (from the '.' column):
- **n**: 36.90%
- **h**: 31.63%
- **x**: 23.53%

Least likely ending letters (non-zero):
- **p**: 3.22%
- **c**: 2.75%
- **j**: 2.45%

Some letters are clearly much more likely to end names — 'n' ends over a third of all names, and 'h' ends nearly a third (think names like Hannah, Leah, Sarah). By contrast, names rarely end in consonants like 'j', 'c', or 'p'.

## 3. Are there any letters following 'q' other than 'u'?

Yes — while 'u' is by far the most common (206 times), 'q' is followed by many other letters in the dataset:
- 'a': 13 times
- 'i': 13 times
- 's': 2 times, 'o': 2 times, 'm': 2 times, 'w': 3 times
- 'e', 'l', 'r': 1 time each
- '.': 28 times (meaning 'q' ends a name)

This likely reflects names from Arabic, Chinese, or other languages transliterated into English where 'q' doesn't require a following 'u'.

## 4. Most likely second letter for names starting with 'x'

The most likely second letter for names starting with 'x' is **'a'** (14.78%), followed closely by **'i'** (14.63%). This reflects names like Xander, Xavi, Xavier, Xiao, etc.

## 5. Do the 25 statistically-generated names seem realistic?

The names are a mixed bag. Some are plausible and even sound like real names: *jaylon*, *jale*, *tien*, *olya*, *dan*, *mir*, *staman*. Others are clearly not realistic: *siquxxtal*, *mbllilicakaisa*, *ayriaynige*, *kexijahak*. 

The bigram model captures basic letter-pair patterns well (common endings like '-on', '-an', '-ayla'), but it has no memory beyond the previous letter. This means it can produce long runs of rare combinations that would never appear in a real name. A real language model considers much longer context, which is why makemore produces far more convincing outputs.

## 6. How does the makemore heatmap compare to the real-names heatmap?

**Similarities:** Both heatmaps show the same broad structural patterns — vowels (a, e, i, o) appear frequently as the second letter after most consonants, and the high-probability starting letters (a, k, m) are consistent across both. Common endings like 'n' and 'h' remain prominent in the makemore output.

**Differences:** The makemore heatmap is sparser and noisier because it's built from only 249 names versus 32,000, so many bigram cells are empty or based on very few observations. More importantly, makemore's names show smoother, more naturalistic transitions — the model learned higher-order patterns (not just pairs) during training, so its output avoids the jarring letter combinations that appear in the purely statistical generator. For example, the makemore names rarely produce impossible-looking consonant clusters because the transformer attends to the full name context, not just the last letter.
