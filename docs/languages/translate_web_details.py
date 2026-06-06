import os
import re
from googletrans import Translator
import time

def main():
    lang_dir = "/home/elezeta/brain/cortexrush/docs/languages"
    translator = Translator()
    
    # Original texts
    version_en = "Version:"
    date_en = "Date:"
    size_en = "Size:"
    
    lang_files = [f for f in os.listdir(lang_dir) if f.startswith("lang") and f.endswith(".js") and f != "lang.js" and f != "langen.js"]
    
    for fn in lang_files:
        lang_code = fn[4:-3]  # lang<CODE>.js
        
        # translate the texts
        try:
            # handle some special cases for language codes
            gt_code = lang_code
            if gt_code in ["apc", "apd", "arq", "ary", "arz"]:
                gt_code = "ar"
            if gt_code in ["wuu", "yue"]:
                gt_code = "zh-CN"
            if gt_code == "pcm":
                gt_code = "en"
                
            version_trans = translator.translate(version_en, dest=gt_code).text if gt_code != "en" else version_en
            date_trans = translator.translate(date_en, dest=gt_code).text if gt_code != "en" else date_en
            size_trans = translator.translate(size_en, dest=gt_code).text if gt_code != "en" else size_en
            
            if not version_trans: version_trans = version_en
            if not date_trans: date_trans = date_en
            if not size_trans: size_trans = size_en
            
        except Exception as e:
            print(f"Error translating for {lang_code}: {e}")
            version_trans = version_en
            date_trans = date_en
            size_trans = size_en
            
        filepath = os.path.join(lang_dir, fn)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # We need to replace DOWNLOAD_VERSION_INFO with the new strings.
        # It looks like: "DOWNLOAD_VERSION_INFO": "...",
        v_trans_esc = version_trans.replace('"', '\\"')
        d_trans_esc = date_trans.replace('"', '\\"')
        s_trans_esc = size_trans.replace('"', '\\"')
        replacement = f'"DOWNLOAD_VERSION": "{v_trans_esc}",\n    "DOWNLOAD_DATE": "{d_trans_esc}",\n    "DOWNLOAD_SIZE": "{s_trans_esc}",'
        
        content = re.sub(r'"DOWNLOAD_VERSION_INFO"\s*:\s*".*?",', replacement, content)
        
        # write back
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Updated {fn}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
