import nltk
import json
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

import Twitter.util


def main():
    classifier = init_classifier()

    for i in range(1, 39):

        currentFile = "GW_Tweets2/" + str(i) + ".json"
        print("GAMEWEEK " + str(i) + "\n")
        with open(currentFile, 'r') as f:
            data = f.readlines()
            data = [x.strip() for x in data]

        for tweet in data:
            # preprocess(tweet)
            # get_human_names(tweet)
            for name in targetNames:
                if (name in tweet):
                    print(tweet)
                    calculateScore(classifier, tweet)


def calculateScore(classifier, tweet):
    overallScore = {}
    overallScore['pos'] = 0
    overallScore['neg'] = 0

    text = [Twitter.util.strip_punctuation(w.lower()) for w in nltk.word_tokenize(tweet) if
            w.lower() not in stopwords]
    score = Twitter.util.classify(classifier, text)
    tClass = max(score, key=score.get)

    # Add to classification score
    overallScore[tClass] += 1

    decision = "No Tweets. Check back in later."
    # if # of tweets > 0
    if overallScore['neg'] + overallScore['pos'] != 0:
        decision = max(overallScore, key=overallScore.get)
        # Sit if not enough tweets
        # Tie = sit
        if overallScore['pos'] == overallScore['neg']:
            decision = 'Sit'
        elif decision == 'pos':
            decision = 'Start'
        else:
            decision = 'Sit'

    return json.dumps({'status': 'OK', 'tweets': text, 'score': overallScore, 'decision': decision})


def init_classifier():
    training_path = 'Training/'
    test_path = "Test/"

    return Twitter.util.initClassifier(training_path, stopwords)


# Gets all names but also many words due to twitter text.
# Could be used as first filter and check each found name with all player names
# But also need to understand sentiment.
def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)

    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:  # avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []


if __name__ == '__main__':
    person_list = []
    person_names = person_list

    targetNames = ["Salah"]

    stopwords = ['a', 'about', 'after', 'am', 'an', 'and', 'any', 'as', 'at', 'be', 'because', 'been', 'by', 'both',
                 'but', 'during', 'each', 'between', 'being', 'did', 'do', 'does', 'doing', 'for', 'from', 'further',
                 'had', 'has', 'have', 'he', 'hed', 'hell', 'hes', 'her', 'here', 'heres', 'hers', 'herself', 'him',
                 'himself', 'his', 'how', 'hows', 'i', 'im', 'id', 'ill', 'having', 'ive', 'if', 'in', 'into', 'is',
                 'it', 'its', 'its', 'itself', 'lets', 'me', 'my', 'myself', 'of', 'on', 'or', 'our', 'ours',
                 'ourselves', 'own', 'same', 'she', 'shed', 'shell', 'shes', 'so', 'such', 'than', 'that', 'thats',
                 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd',
                 'theyll', 'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'very', 'was', 'we', 'wed',
                 'well', 'were', 'weve', 'were', 'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which', 'while',
                 'who', 'whos', 'whom', 'why', 'whys', 'with', 'you', 'youd', 'youll', 'youre', 'youve', 'your',
                 'yours', 'yourself', 'yourselves', 'quarterback', 'qb', 'qbs', 'rb', 'rbs', 'receiver', 'wr', 'wrs',
                 'te', 'tes', 'k', 'ks', 'kicker', 'fantasy', 'football', 'team', 'points', 'nfl']

    nltk.download('punkt', download_dir='D:\\nltk_data')
    nltk.download('averaged_perceptron_tagger', download_dir='D:\\nltk_data')
    nltk.download('maxent_ne_chunker', download_dir='D:\\nltk_data')
    nltk.download('words', download_dir='D:\\nltk_data')
    main()
