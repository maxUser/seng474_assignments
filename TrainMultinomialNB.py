def main():
    # C = all classes; c = one class
    # D = entire document; d = one line
    # V = vocabulary
    # N = number of lines?
    train_data = open("traindata.txt", "r")
    train_labels = open("trainlabels.txt", "r")

    # Classes
    # 0 = wise
    # 1 = future
    classes = (0, 1)
    vocab = []
    num_lines = 0
    docs_in_class = 0
    prior_c = []
    count = 0
    future_phrases = []
    wise_phrases = []

    for line in train_data:
        vocab.extend(line.split()) # V <- ExtractVocabulary(D)
        # print(line)
        num_lines = num_lines + 1
        if count < 152:
            future_phrases.extend(line.rstrip('\n').split('\n'))
        elif count > 151:
            wise_phrases.extend(line.rstrip('\n').split('\n'))
        count = count + 1

    num_words = len(vocab) # N <- CountDocs(D)

    # label info
    num_wise = 0
    num_future = 0

    for line in train_labels:
        if '0' in line:
            num_wise = num_wise + 1
        if '1' in line:
            num_future = num_future + 1

    for c in classes: # for each c in C
        for i in range(10):
            print('X', '\n')
        # do Nc <- CountDocsInClass(D, c)
        Nc = 0 # number of phrases per class
        if c == 0:
            Nc = num_wise
        elif c == 1:
            Nc = num_future

        prior_c.append(Nc/num_lines) # prior[c] <- Nc/N

        textc = ''# textc <- ConcatenateTextOfAllDocsInClass(D, c)
        if c == 0:
            textc = ' '.join(str(phrase) for phrase in wise_phrases)
        elif c == 1:
            textc = ' '.join(str(phrase) for phrase in future_phrases)

        Tct = 0
        for term in vocab: # for each t in V
            # do Tct <- CountTokensOfTerm(textc, t)
            # Tct = number of occurrences of t in training docs from class c
            if term in textc:
                Tct = Tct + 1
        print(len(textc))
        print(Tct)
        for term in vocab: # for term in vocab: # for each t in V
            # do condprob[t][c] <- (Tct + 1) / ()










if __name__ == "__main__":
    main()
