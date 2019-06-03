from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions, EmotionOptions, SyntaxOptions, SyntaxOptionsTokens, CategoriesOptions
import json

# If service instance provides API key authentication
service = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api',
    iam_apikey='XGAX8S8S4uHsl36azpgu6stnZ8RaBJ_bpoHDdTtRfS4e')

response = service.analyze(
    text='Alli and Lloris ruled out - Son is back and could play a part - Vardy is back from 3 match suspension - Zaha and Tomkins back in training',
    features=Features(sentiment=SentimentOptions(targets=['Alli', 'Lloris','Vardy', 'Zaha']))).get_result()

print(json.dumps(response, indent=2))
