// Cortex Rush Multi-Language Support Script

const supportedLanguages = ['am', 'apc', 'apd', 'ar', 'arq', 'ary', 'arz', 'az', 'bho', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'eo', 'es', 'eu', 'fa', 'fi', 'fr', 'gl', 'gu', 'ha', 'he', 'hi', 'hu', 'id', 'it', 'ja', 'jv', 'kn', 'ko', 'ml', 'mr', 'my', 'nl', 'no', 'or', 'pa', 'pcm', 'pl', 'pt', 'ro', 'ru', 'sk', 'su', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'uz', 'vi', 'wuu', 'yo', 'yue', 'zh'];

function getLanguage() {
    // Check for query parameter override
    const urlParams = new URLSearchParams(window.location.search);
    const langParam = urlParams.get('lang');
    if (langParam && supportedLanguages.includes(langParam)) {
        return langParam;
    }
    
    // Auto-determine from navigator (browser settings)
    const browserLang = (navigator.language || navigator.userLanguage).split('-')[0];
    if (supportedLanguages.includes(browserLang)) {
        return browserLang;
    }
    
    // Default to English
    return 'en';
}

function loadLanguage(lang) {
    // Determine the base path based on current location
    // If we're inside /privacy/, we need to go up one directory
    const isInSubdir = window.location.pathname.includes('/privacy/');
    const basePath = isInSubdir ? '../' : '';
    
    const script = document.createElement('script');
    script.src = basePath + `languages/lang${lang}.js`;
    script.onload = applyTranslations;
    script.onerror = () => {
        document.body.style.visibility = 'visible';
    };
    document.head.appendChild(script);
}

function applyTranslations() {
    if (typeof langData !== 'undefined') {
        // Update Meta Description
        const isInSubdir = window.location.pathname.includes('/privacy/');
        const descKey = isInSubdir ? 'PRIVACY_META_DESC' : 'META_DESC';
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc && langData[descKey]) {
            metaDesc.content = langData[descKey];
        }
        
        // Replace content in elements marked with data-i18n
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (langData[key]) {
                // If it's an image, replace the alt text instead of inner HTML
                if (el.tagName === 'IMG') {
                    el.alt = langData[key];
                } else {
                    el.innerHTML = langData[key];
                }
            }
        });
    }
    
    // Always make body visible after translations are applied (or if langData is undefined)
    document.body.style.visibility = 'visible';
}

document.addEventListener('DOMContentLoaded', () => {
    const lang = getLanguage();
    loadLanguage(lang);
    
    // Update all internal links to propagate the ?lang= parameter if we are forcing a language
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('lang')) {
        const forceLang = urlParams.get('lang');
        document.querySelectorAll('a').forEach(a => {
            const href = a.getAttribute('href');
            // Only modify relative links
            if (href && !href.startsWith('http') && !href.startsWith('//') && !href.startsWith('#')) {
                // Determine base URL to parse properly
                const url = new URL(a.href, window.location.href);
                url.searchParams.set('lang', forceLang);
                a.href = url.pathname + url.search + url.hash;
            }
        });
    }
});
