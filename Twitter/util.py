import nltk
import os
import re
import math
import codecs
from string import punctuation


# Removes punctuation
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)


# Retrieves training document tokens/classes
def getTrainingDocs(training_path, stopwords):
    classes = []
    docTokens = {}
    classDocs = {}
    # Iterate through training documents
    for file in os.listdir(training_path):
        # Get class name from file name.
        if not file.startswith('.'):
            className = re.match(r'^[a-zA-Z]+', file).group(0)
            classes.append(className)
            # initialize document list for each class
            if not className in classDocs:
                classDocs[className] = []
            # Get text from file
            fOpen = codecs.open(training_path + file, 'r', encoding='utf-8', errors='ignore')
            fRead = fOpen.readlines()
            docIndex = 1
            for tweet in fRead:
                # tweet name "<class><index>"
                docName = className + str(docIndex)
                classDocs[className].append(docName)
                docTokens[docName] = [strip_punctuation(w.lower()) for w in nltk.word_tokenize(tweet) if
                                      w.lower() not in stopwords]
                docIndex += 1
    return {'classes': set(classes), 'docs': docTokens, 'classDocs': classDocs}


# Trains the classifier using the training documents
def trainClassifier(classifier):
    classes = classifier['classes']
    docs = classifier['docs']
    classDocs = classifier['classDocs']
    vocab = classifier['vocab']

    numDocs = len(docs)
    prior = {}
    classText = {}
    tct = {}
    condprob = {}

    for c in classes:
        # Calculate prior
        prior[c] = float(len(classDocs[c])) / float(numDocs)
        # Concatenate text in all documents in the classs
        classText[c] = []
        for doc in classDocs[c]:
            classText[c] = classText[c] + docs[doc]
        # Count # of tokens for each term
        tct[c] = {}
        for term in vocab:
            tct[c][term] = classText[c].count(term)
        # Calculate condprob[term][c]
        tctSum = 0
        for term in tct[c]:
            tctSum += (tct[c][term] + 1)
        for term in vocab:
            if term not in condprob:
                condprob[term] = {}
            condprob[term][c] = float((tct[c][term] + 1)) / float(tctSum)
    return {'prior': prior, 'condprob': condprob}


# Creates the naive bayes classifier
def initClassifier(training_path, stopwords):
    # Get training information
    classifier = getTrainingDocs(training_path, stopwords)

    # Get vocab
    vocab = set()
    for key in classifier['docs']:
        vocab = vocab.union(classifier['docs'][key])
    classifier['vocab'] = vocab

    # Train Classifier
    trainingInfo = trainClassifier(classifier)
    classifier['prior'] = trainingInfo['prior']
    classifier['condprob'] = trainingInfo['condprob']
    return classifier


# Classifies document d based on the classifier
def classify(classifier, d):
    classes = classifier['classes']
    vocab = classifier['vocab']
    prior = classifier['prior']
    condprob = classifier['condprob']

    score = {}
    for c in classes:
        score[c] = math.log(prior[c])
        for t in d:
            if t in condprob:
                score[c] += math.log(condprob[t][c])
    # return max(score, key=score.get)
    return score
