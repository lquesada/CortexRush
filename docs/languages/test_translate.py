import os
from googletrans import Translator

translator = Translator()
text = "Support me by listening to my music project Windlereye"

for lang in ['de', 'es', 'ru', 'zh-CN', 'ja', 'ar', 'ur']:
    try:
        trans = translator.translate(text, dest=lang).text
        print(f"{lang}: {trans}")
    except Exception as e:
        print(e)
