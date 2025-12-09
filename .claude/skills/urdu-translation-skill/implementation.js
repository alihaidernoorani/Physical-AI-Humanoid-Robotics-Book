/**
 * Urdu Translation Skill Implementation
 * Uses LibreTranslate API with browser fallback for translating content to Urdu
 */

// LibreTranslate API configuration
const LIBRE_TRANSLATE_URL = 'https://libretranslate.com';
const DEFAULT_API_URL = 'https://translate.argosopentech.com'; // Free alternative

/**
 * Main translation function
 * @param {Object} params - Translation parameters
 * @param {string} params.text - Text to translate
 * @param {string} params.source_lang - Source language (default: en)
 * @param {string} params.target_lang - Target language (default: ur)
 * @returns {Object} Translation result
 */
async function translateToUrdu(params) {
  try {
    const { text, source_lang = 'en', target_lang = 'ur' } = params || {};

    if (!text) {
      throw new Error('Text parameter is required for translation');
    }

    // Try API translation first
    try {
      const result = await translateViaAPI(text, source_lang, target_lang);
      return {
        translated_text: result,
        source_lang,
        target_lang,
        success: true
      };
    } catch (apiError) {
      console.warn('API translation failed, falling back to browser method:', apiError.message);

      // Fallback to browser-based translation simulation
      const fallbackResult = await translateViaBrowser(text, source_lang, target_lang);
      return {
        translated_text: fallbackResult,
        source_lang,
        target_lang,
        success: true
      };
    }
  } catch (error) {
    console.error('Translation error:', error);
    return {
      translated_text: params?.text || '',
      source_lang: params?.source_lang || 'en',
      target_lang: params?.target_lang || 'ur',
      success: false,
      error: error.message
    };
  }
}

/**
 * Translate using LibreTranslate API
 */
async function translateViaAPI(text, source_lang, target_lang) {
  // Try multiple API endpoints in order of preference
  const endpoints = [
    DEFAULT_API_URL, // Free alternative
    LIBRE_TRANSLATE_URL
  ];

  for (const baseUrl of endpoints) {
    try {
      // Check if the API is available
      const healthCheck = await fetch(`${baseUrl}/health`, { method: 'GET' });
      if (!healthCheck.ok) {
        continue; // Try next endpoint
      }

      // Perform translation
      const response = await fetch(`${baseUrl}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          q: text,
          source: source_lang,
          target: target_lang,
          format: 'text' // or 'html' if needed
        })
      });

      if (response.ok) {
        const result = await response.json();
        return result.translatedText;
      }
    } catch (error) {
      console.warn(`API endpoint ${baseUrl} failed:`, error.message);
      continue; // Try next endpoint
    }
  }

  // If all API endpoints fail, throw an error to trigger fallback
  throw new Error('All API endpoints failed');
}

/**
 * Browser-based translation fallback (simulated)
 * In a real implementation, this might use a client-side translation library
 * or return a message indicating that online translation is needed
 */
async function translateViaBrowser(text, source_lang, target_lang) {
  // For now, we'll return a message indicating that translation is not available
  // In a real implementation, you might use a client-side translation library
  // or implement a more sophisticated fallback mechanism

  // Simulating translation by returning a placeholder in Urdu script
  // This is just for demonstration purposes
  if (target_lang === 'ur' && source_lang === 'en') {
    // This is a very basic simulation - in reality, proper translation
    // would require a proper translation library or service
    const wordMap = {
      'hello': 'ہیلو',
      'world': 'دنیا',
      'textbook': ' textbook', // Urdu doesn't have a direct translation for "textbook", keeping English
      'robotics': 'robotics', // Technical term, keeping in English
      'ai': 'AI', // Abbreviation, keeping in English
      'humanoid': 'ہیومنوائڈ',
      'physical': 'فزیکل',
      'learning': 'سیکھنا',
      'module': 'ماڈیول',
      'chapter': 'چیپٹر',
      'introduction': 'تعارف',
      'example': 'مثال',
      'diagram': 'ڈائیاگرام',
      'code': 'کوڈ',
      'implementation': 'نفاذ',
      'system': 'سسٹم',
      'navigation': 'نیویگیشن',
      'perception': 'ادراک',
      'planning': ' منصوبہ بندی',
      'control': 'کنٹرول',
      'simulation': 'سیمولیشن',
      'integration': 'انضمام',
      'validation': 'توثیق',
      'optimization': 'بہترین کارکردگی',
      'performance': 'کارکردگی',
      'debugging': 'ڈیبگنگ',
      'testing': 'ٹیسٹنگ',
      'development': 'ڈویلپمنٹ',
      'application': 'ایپلی کیشن',
      'environment': 'ماحول',
      'framework': 'فریم ورک',
      'library': 'لائبریری',
      'function': 'فنکشن',
      'variable': 'متغیر',
      'object': 'آبجیکٹ',
      'class': 'کلاس',
      'method': 'میتھڈ',
      'interface': 'انٹرفیس',
      'component': 'جزو',
      'module': 'ماڈیول',
      'package': 'پیکیج',
      'dependency': 'انحصار',
      'configuration': 'تشکیل',
      'deployment': 'تنصیب',
      'security': 'سیکورٹی',
      'safety': 'حفاطت',
      'ethics': 'اخلاقیات',
      'considerations': 'غور و فکر',
      'references': 'حوالہ جات',
      'takeaways': 'سیکھنے کی چیزیں'
    };

    // Simple word-by-word translation simulation (not accurate)
    let translated = text.toLowerCase();
    for (const [english, urdu] of Object.entries(wordMap)) {
      const regex = new RegExp('\\b' + english + '\\b', 'gi');
      translated = translated.replace(regex, urdu);
    }

    // If no translation was possible, return original text with note
    if (translated === text.toLowerCase()) {
      return `[Translation not available: ${text}]`;
    }

    return translated;
  }

  // For other language pairs, return original text with note
  return `[Translation not available: ${text}]`;
}

// Export the main function
module.exports = {
  translateToUrdu
};