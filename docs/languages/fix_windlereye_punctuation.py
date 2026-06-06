import os
import re

def main():
    lang_dir = "/home/elezeta/brain/cortexrush/docs/languages"
    
    lang_files = [f for f in os.listdir(lang_dir) if f.startswith("lang") and f.endswith(".js")]
    
    for fn in lang_files:
        filepath = os.path.join(lang_dir, fn)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Fix the characters before <a href=...
        # We strip period (.), ideographic full stop (。), Urdu period (\u06D4), Devanagari danda (\u0964), and spaces
        pattern_before = r'[\.\u3002\u06D4\u0964\s]*<a href=\\"https://www\.windlereye\.com\\"'
        content = re.sub(pattern_before, ' <a href=\\"https://www.windlereye.com\\"', content)
        
        # Also clean up any punctuation added after </a>
        pattern_after = r'</a>[\.\u3002\u06D4\u0964\s]*",'
        content = re.sub(pattern_after, '</a>",', content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    main()
