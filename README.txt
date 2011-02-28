CruftStripper
-------------

== Process

Convert HTML into lines, each containing a paragraph of text

Remove non-sentences:

for each line:
 sentences = Split lines by periods

 for each sentence:
  sentence_total += len(sentence)

  if Doesn't start with a capital letter?:
   continue

  words = Split sentence by spaces, punctuation
  if len(words)<4?:
   continue

  for each word:
    word_total += len(word)
    if Not all letters?:
     continue
    if len(word)<=2 and not common short word?:
     continue
    word_score += len(word)

  if word_score/word_total>word_threshold?:
   sentence_score += len(sentence)

 if sentence_score/sentence_total>sentence_threshold?:
  result.append(line)