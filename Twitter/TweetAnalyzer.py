import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag


def main():
    for i in range(1, 39):
        currentFile = "GW_Tweets2/" + str(i) + ".json"
        print("GAMEWEEK "+str(i)+"\n")
        with open(currentFile, 'r') as f:
            data = f.readlines()
            data = [x.strip() for x in data]

        for tweet in data:
            # preprocess(tweet)
            #get_human_names(tweet)
            for name in targetNames:
                if(name in tweet):
                    print(tweet)



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


    nltk.download('punkt', download_dir='D:\\nltk_data')
    nltk.download('averaged_perceptron_tagger', download_dir='D:\\nltk_data')
    nltk.download('maxent_ne_chunker', download_dir='D:\\nltk_data')
    nltk.download('words', download_dir='D:\\nltk_data')
    main()
