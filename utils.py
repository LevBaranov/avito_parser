from pprint import pprint

def compare(s1, s2):
    s1, s2 = [ s.lower() for s in [s1,s2] ]
    ngrams = [ s1[i:i+3] for i in range(len(s1)-1) ]
    count = 0
    for ngram in ngrams:
        count += s2.count(ngram)
    return count / max(len(s1),len(s2))

if __name__ == '__main__':
    out = []
    for a,b in [
            ('алгоритм','алгоритм'),
            ('алгоритм','алгоритмы'),
            ('алгоритм','алгоритмов'),
            ('стол','столик'),
            ('стол','стул'),
            ('маша','даша'),
            ('ольга','олег'),
            ('ольга','оля'),
            ('маша','машенька'),
        ]:
        out += [(a,b,compare(a,b))]
    pprint(out)