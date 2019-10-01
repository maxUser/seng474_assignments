from argparse import ArgumentParser
import math


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

    words = []
    for d in docs:
        for word in d.split():
            words.append(word)

    return words


def countTokensOfTerm(textc, t):
    '''Given a term, count how many times it appears in the text'''
    return textc.count(t)


def formula(Tct, textc, V):
    '''Conditional probability + LaPlace smoothing'''
    numerator = Tct + 1
    denominator = len(textc) + len(V)
    condprob = float(numerator) / float(denominator)

    return condprob


def extractTokensFromDoc(V, d):
    '''Extract tokens matching the document'''
    return [word for word in d.split() if word in V]


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
            condprob[t][c] = formula(Tct, textc, V)

    return V, prior, condprob


def compareResults(results, expected):
    '''Given 2 lists of booleans return the percent of matching items'''
    total = [True if result == expect else False for result, expect in zip(results, expected)]
    # get total instances of a match
    matching = 0
    for bool in total:
        if bool:
            matching += 1

    # return accuracy in percent
    return (float(matching) / float(len(total))) * 100


def applyMultinomialNB(C, V, prior, condprob, d):
    '''Apply the trained values to the documents'''
    W = extractTokensFromDoc(V, d)
    score = [None, None]
    for c in C:
        score[int(c)] = math.log(prior[int(c)], 2)

        for t in W:
            score[int(c)] += math.log(condprob[t][c])
    # the score corresponds to the class which the doc is more likely to be in
    # cast index to string for final comparison
    return str(score.index(max(score)))


if __name__ == '__main__':
    # We need to do a little prep before running the algo
    data, labels = getArgs()
    D = mapAllDocs(data, labels)
    C = getAllClasses(labels)
    result = []
    accuracy = -1

    # run training
    V, prior, condprob = trainMultinomialNB(C, D)

    testOrTrain = input('test or train: ')

    if testOrTrain == 'train':
        # apply MNB and store result
        result = [applyMultinomialNB(C, V, prior, condprob, d['doc']) for d in D]
        # turn labels into list for final comparison
        accuracy = compareResults(result, fileToList(labels))
    elif testOrTrain == 'test':
        D = mapAllDocs('testdata.txt', 'testLabels.txt')
        C = getAllClasses('testLabels.txt')
        result = [applyMultinomialNB(C, V, prior, condprob, d['doc']) for d in D]
        accuracy = compareResults(result, fileToList('testLabels.txt'))

    # final output
    print('Accuracy: {}%'.format(accuracy))
