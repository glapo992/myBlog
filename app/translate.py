import requests
from flask_babel import _
from app import current_app

def translate(text:str, source_language:str, dest_language:str)->str:
    """translate a text from the original lang to a target lang with Microsoft API

    :param text: the text to translate
    :type text: str
    :param source_language: the code of the source language
    :type source_language: str
    :param dest_language: code of the target lang
    :type dest_language: str
    :return: text translated
    :rtype: str
    """
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: translation service not configured') 
    # from microsoft documentation for api connection
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'westus2'}
    # send a post request to microsoft API
    r = requests.post('https://api.cognitive.microsofttranslator.com'
        '/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[{'Text': text}])
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return r.json()[0]['translations'][0]['text']