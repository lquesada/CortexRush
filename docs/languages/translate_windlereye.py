import os
import re
from googletrans import Translator
import time

def main():
    lang_dir = "/home/elezeta/brain/cortexrush/docs/languages"
    translator = Translator()
    
    text_en = "Support me by listening to my music project Windlereye"
    html_link = '<a href=\\"https://www.windlereye.com\\" target=\\"_blank\\" style=\\"color: var(--primary-color);\\">Windlereye</a>'
    
    lang_files = [f for f in os.listdir(lang_dir) if f.startswith("lang") and f.endswith(".js") and f != "lang.js" and f != "langen.js"]
    
    for fn in lang_files:
        lang_code = fn[4:-3]  # extract code
        
        try:
            gt_code = lang_code
            if gt_code in ["apc", "apd", "arq", "ary", "arz"]:
                gt_code = "ar"
            if gt_code in ["wuu", "yue"]:
                gt_code = "zh-CN"
            if gt_code == "pcm":
                gt_code = "en"
                
            if gt_code == "en":
                trans = text_en
            else:
                trans = translator.translate(text_en, dest=gt_code).text
                if not trans:
                    trans = text_en
                    
            # Strip trailing punctuation
            trans = re.sub(r'[\.\u3002\u06D4\u0964\u0965]+$', '', trans).strip()
            
            # Replace Windlereye with the HTML link
            if "Windlereye" in trans:
                final_html = trans.replace("Windlereye", html_link)
            elif "windlereye" in trans.lower():
                # case-insensitive replace
                pattern = re.compile("windlereye", re.IGNORECASE)
                final_html = pattern.sub(html_link, trans)
            else:
                # fallback
                trans_fallback = translator.translate("Support me by listening to my music project ", dest=gt_code).text
                trans_fallback = re.sub(r'[\.\u3002\u06D4\u0964\u0965\s]+$', '', trans_fallback)
                final_html = trans_fallback + " " + html_link
                
        except Exception as e:
            print(f"Error translating for {lang_code}: {e}")
            final_html = text_en.replace("Windlereye", html_link)
            
        filepath = os.path.join(lang_dir, fn)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace the WINDLEREYE_SUPPORT line using regex
        # We look for "WINDLEREYE_SUPPORT": "...",
        replacement = f'"WINDLEREYE_SUPPORT": "{final_html}",'
        content = re.sub(r'"WINDLEREYE_SUPPORT"\s*:\s*".*?",', replacement, content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Updated {fn}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
