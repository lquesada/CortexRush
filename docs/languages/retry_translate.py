import os
import re
from googletrans import Translator
import time

def main():
    lang_dir = "/home/elezeta/brain/cortexrush/docs/languages"
    translator = Translator()
    
    text_en = "Support me by listening to my music project Windlereye"
    html_link = '<a href=\\"https://www.windlereye.com\\" target=\\"_blank\\" style=\\"color: var(--primary-color);\\">Windlereye</a>'
    
    failed_langs = ['sv', 'am', 'fr', 'nl', 'yo']
    
    for lang_code in failed_langs:
        fn = f"lang{lang_code}.js"
        gt_code = lang_code
        try:
            trans = translator.translate(text_en, dest=gt_code).text
            if not trans: trans = text_en
            
            trans = re.sub(r'[\.\u3002\u06D4\u0964\u0965]+$', '', trans).strip()
            
            if "Windlereye" in trans:
                final_html = trans.replace("Windlereye", html_link)
            elif "windlereye" in trans.lower():
                pattern = re.compile("windlereye", re.IGNORECASE)
                final_html = pattern.sub(html_link, trans)
            else:
                trans_fallback = translator.translate("Support me by listening to my music project ", dest=gt_code).text
                trans_fallback = re.sub(r'[\.\u3002\u06D4\u0964\u0965\s]+$', '', trans_fallback)
                final_html = trans_fallback + " " + html_link
                
            filepath = os.path.join(lang_dir, fn)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            replacement = f'"WINDLEREYE_SUPPORT": "{final_html}",'
            content = re.sub(r'"WINDLEREYE_SUPPORT"\s*:\s*".*?",', replacement, content)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"Updated {fn}")
        except Exception as e:
            print(f"Failed {fn}: {e}")
            
if __name__ == "__main__":
    main()
