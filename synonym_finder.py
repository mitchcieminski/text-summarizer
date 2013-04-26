import markov

(markov, wordloc) = markov.build_markov('testdata/1342.txt')

thing = normalize(markov) * normalize(markov.transpose())

thing2 = thing ** 100

print thing2
