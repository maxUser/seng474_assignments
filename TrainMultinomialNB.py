from argparse import ArgumentParser


def getArgs():
    '''Get the filepaths needed to run algo'''
    parser = ArgumentParser()
    parser.add_argument('--data', help='text file containing strings')
    parser.add_argument('--labels', help='text file containing classes')
    args = parser.parse_args()
    return args.data, args.labels


def fileToList(filename):
    '''Helper function to turn text files to lists'''
    return [line.rstrip('\n') for line in open(filename, 'r').readlines()]


def mapAllDocs(data, labels):
    '''Return a list of dictionaries containing mapped lines (docs) to classes

       Each item in the list of the final output will be of the form:
       {'doc': 'some string from text file', 'class': classIdentifier}
    '''
    # first turn both files into lists
    docs = fileToList(data)
    classes = fileToList(labels)

    # they should be the same length
    assert len(docs) == len(classes)

    # create a final list that maps the two together into a dictionary
    mapped = []
    for d, c in zip(docs, classes):
        temp = {'doc': d, 'class': c}
        mapped.append(temp)

    return mapped


def getAllClasses(labels):
    '''Returns a set of the unique classes from text file'''
    return {c for c in fileToList(labels)}


def extractVocabulary(D):
    '''Returns a set of unique words from ALL docs'''
    # brain is too dead to figure out how to set comp this
    vocab = set()
    for line in D:
        for word in line['doc'].split():
            vocab.add(word)

    return vocab


def countDocs(D):
    '''Get TOTAL number of docs'''
    return float(len(D))


def filterOnClass(li, c):
    '''Filter our big list by the class, return a filtered list'''
    return [item for item in li if item['class'] == c]


def countDocsInClass(D, c):
    '''Return a count of the docs with the given class'''
    return float(len(filterOnClass(D,c)))


def concatenateTextOfAllDocsInClass(D, c):
    '''Return a list of all the words in the given class'''
    # extract all the docs so we can mush it all together
    filtered = filterOnClass(D, c)
    docs = [item['doc'] for item in filtered]

    # @Maxi do we need to take just the unique words from here?
    # Based on the algo I don't think so but it wouldn't be hard to change if we do.
    words = []
    for d in docs:
        for word in d.split():
            words.append(word)

    return words


def countTokensOfTerm(textc, t):
    '''Givem a term, count how many times it appears in the text'''
    return textc.count(t)

def formula(Tct, t):
    '''TODO IMPLEMENT THE FORMULA'''
    # temp
    import random
    return random.randint(0,5)


def trainMultinomialNB(C, D):
    '''Honestly I'm not really sure what this section does, just following notes

       C = all classes; c = one class
        These are stored as a set
       D = entire document; d = one line
        These are stored in a list of dictionaries
    '''
    V = extractVocabulary(D)
    N = countDocs(D)

    # we need to define some vars for this loop
    prior = [None] * len(C)   # define an empty list with length of num classes
    condprob = {t:{} for t in V}    # define a dictionary of the terms with empty dict to be filled out

    for c in C:
        Nc = countDocsInClass(D, c)
        prior[int(c)] = Nc/N
        textc = concatenateTextOfAllDocsInClass(D, c)

        for t in V:
            Tct = countTokensOfTerm(textc, t)
            condprob[t][c] = formula(Tct, t)    # todo

    return V, prior, condprob


def applyMultinomialNB(C, V, prior, condprob, d):
    # I don't have the patiene for this right now
    return 0


if __name__ == '__main__':
    # We need to do a little prep before running the algo
    data, labels = getArgs()
    D = mapAllDocs(data, labels)
    C = getAllClasses(labels)


    # run the first part of the algo
    V, prior, condprob = trainMultinomialNB(C, D)

    print('V: {}'.format(V))
    print('prior: {}'.format(prior))
    print('condprob: {}'.format(condprob))
