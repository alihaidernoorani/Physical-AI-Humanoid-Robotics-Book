// Translation utilities for Urdu translation service

// LibreTranslate API configuration
const LIBRE_TRANSLATE_API_URL = 'https://libretranslate.com/translate';
const DEFAULT_API_URL = LIBRE_TRANSLATE_API_URL;

/**
 * Translate text using LibreTranslate API
 * @param {string} text - Text to translate
 * @param {string} sourceLang - Source language code (default: 'en')
 * @param {string} targetLang - Target language code (default: 'ur')
 * @returns {Promise<Object>} Translation result
 */
export const translateText = async (text, sourceLang = 'en', targetLang = 'ur') => {
  try {
    // First try the LibreTranslate API
    const response = await fetch(DEFAULT_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        q: text,
        source: sourceLang,
        target: targetLang,
        format: 'text',
      }),
    });

    if (!response.ok) {
      throw new Error(`Translation API error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    return {
      translatedText: result.translatedText,
      success: true,
      error: null
    };
  } catch (error) {
    console.error('Translation error:', error);

    // Fallback: return original text with error info
    return {
      translatedText: text,
      success: false,
      error: error.message
    };
  }
};

/**
 * Check if translation service is available
 * @returns {Promise<boolean>} Service availability
 */
export const isTranslationServiceAvailable = async () => {
  try {
    // Simple check to see if the API is accessible
    const response = await fetch(DEFAULT_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        q: 'test',
        source: 'en',
        target: 'ur',
        format: 'text',
      }),
    });

    return response.ok;
  } catch (error) {
    console.error('Translation service check failed:', error);
    return false;
  }
};

/**
 * Browser-based translation fallback (for when API is unavailable)
 * @param {string} text - Text to translate
 * @returns {string} Translated text (or original if no translation available)
 */
export const browserTranslateFallback = (text) => {
  // This is a placeholder - in a real implementation, you might use the
  // browser's built-in translation capabilities or other client-side methods
  // For now, return the original text
  console.warn('Using browser fallback for translation - API not available');
  return text;
};

/**
 * Cache translation results in localStorage
 * @param {string} key - Cache key (typically a hash of the text)
 * @param {Object} result - Translation result to cache
 * @param {number} ttl - Time to live in minutes (default: 60 minutes)
 */
export const cacheTranslation = (key, result, ttl = 60) => {
  const cacheEntry = {
    result,
    timestamp: Date.now(),
    ttl: ttl * 60 * 1000 // Convert minutes to milliseconds
  };

  try {
    localStorage.setItem(`translation-cache-${key}`, JSON.stringify(cacheEntry));
  } catch (error) {
    console.warn('Failed to cache translation:', error);
  }
};

/**
 * Get cached translation result
 * @param {string} key - Cache key
 * @returns {Object|null} Cached result or null if not found/expired
 */
export const getCachedTranslation = (key) => {
  try {
    const cachedStr = localStorage.getItem(`translation-cache-${key}`);
    if (!cachedStr) return null;

    const cached = JSON.parse(cachedStr);
    const now = Date.now();

    // Check if cache is still valid
    if (now - cached.timestamp < cached.ttl) {
      return cached.result;
    } else {
      // Cache expired, remove it
      localStorage.removeItem(`translation-cache-${key}`);
      return null;
    }
  } catch (error) {
    console.warn('Failed to retrieve cached translation:', error);
    return null;
  }
};

/**
 * Generate cache key for text
 * @param {string} text - Text to generate key for
 * @returns {string} Cache key
 */
export const generateCacheKey = (text, sourceLang = 'en', targetLang = 'ur') => {
  // Simple hash function to generate a key
  let hash = 0;
  const str = `${text}-${sourceLang}-${targetLang}`;

  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }

  return Math.abs(hash).toString();
};