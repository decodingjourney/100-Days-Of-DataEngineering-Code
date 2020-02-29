import string


def subtract(d1, d2):
    res = {}

    for key in d1.keys():
        if key not in d2.keys():
            res[key] = None
    return res


def most_common(hist):
    t = []
    for key, value in hist.items():
        t.append((value, key))

    t.sort()
    t.reverse()
    return t


def different_words(hist):
    return len(hist)


def total_words(hist):
    return sum(hist.values())


def process_line(line, hist):
    line = line.replace('-', ' ')
    for word in line.split():
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()
        hist[word] = hist.get(word, 0) + 1


def skip_gutenberg_header(file_obj):
    for line in file_obj:
        if line.startswith('*END*THE SMALL PRINT!'):
            break


def process_file(filename, skip_header):
    hist = {}
    fp = open(filename)

    if skip_header:
        skip_gutenberg_header(fp)

    for line in fp:
        process_line(line, hist)
    return hist


if __name__ == '__main__':
    histogram = process_file('/home/anand/quantela_projects/learning_basic_python/emma.txt', skip_header=True)

    print('Total number of words in the file is ', total_words(histogram))

    print('Total number of different words are ', different_words(histogram))

    t = most_common(histogram)
    for freq, word in t[0:20]:
        print(word, '\t', freq)

    words = process_file('/home/anand/quantela_projects/learning_basic_python/Exploring_words.txt', skip_header=False)
    diff = subtract(histogram, words)
    print('The word in histogram that are not in word list are ')
    for word in diff.keys():
        print(word)
