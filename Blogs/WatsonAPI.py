from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, SentimentOptions, EmotionOptions, KeywordsOptions, RelationsOptions
import json

# If service instance provides API key authentication
service = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api',
    iam_apikey='XGAX8S8S4uHsl36azpgu6stnZ8RaBJ_bpoHDdTtRfS4e')

response = service.analyze(
    url= "https://www.fantasyfootballscout.co.uk/2019/04/06/vardys-owners-facing-a-tough-choice-ahead-of-double-gameweek-35/",
    features=Features(emotion=EmotionOptions(targets=["Tielemans"]))).get_result()

print(json.dumps(response, indent=2))
