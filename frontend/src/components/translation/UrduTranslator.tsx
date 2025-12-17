import React, { useState, useEffect } from 'react';

interface UrduTranslatorProps {
  content: string;
  onTranslationComplete?: (translatedContent: string) => void;
  onError?: (error: string) => void;
}

const UrduTranslator: React.FC<UrduTranslatorProps> = ({
  content,
  onTranslationComplete,
  onError
}) => {
  const [translatedContent, setTranslatedContent] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Function to translate content to Urdu
  const translateToUrdu = async (): Promise<string> => {
    // In a real implementation, this would call the translation API
    // For now, we'll use a simple word mapping for demonstration
    const wordMap: { [key: string]: string } = {
      'hello': 'ہیلو',
      'world': 'دنیا',
      'textbook': ' textbook', // Keep technical terms in English
      'robotics': 'robotics',
      'ai': 'AI',
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

    // Simple word-by-word translation for demonstration
    let translated = content.toLowerCase();
    for (const [english, urdu] of Object.entries(wordMap)) {
      const regex = new RegExp('\\b' + english + '\\b', 'gi');
      translated = translated.replace(regex, urdu);
    }

    // If no translation occurred, return original content with note
    if (translated === content.toLowerCase()) {
      return `[Translation not available: ${content}]`;
    }

    return translated;
  };

  const handleTranslate = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await translateToUrdu();
      setTranslatedContent(result);

      if (onTranslationComplete) {
        onTranslationComplete(result);
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Translation failed';
      setError(errorMessage);

      if (onError) {
        onError(errorMessage);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Reset when content changes
  useEffect(() => {
    setTranslatedContent(null);
    setError(null);
  }, [content]);

  return {
    translatedContent,
    isLoading,
    error,
    handleTranslate
  };
};

// Separate component for the translation button and display
interface UrduTranslationComponentProps {
  content: string;
}

const UrduTranslationComponent: React.FC<UrduTranslationComponentProps> = ({ content }) => {
  const [showUrdu, setShowUrdu] = useState(false);
  const [originalContent, setOriginalContent] = useState(content);

  const {
    translatedContent,
    isLoading,
    error,
    handleTranslate
  } = UrduTranslator({
    content: originalContent,
    onTranslationComplete: (translated) => {
      setOriginalContent(translated);
      setShowUrdu(true);
    },
    onError: (err) => {
      console.error('Translation error:', err);
    }
  });

  const handleToggleLanguage = () => {
    if (showUrdu) {
      // Switch back to original content
      setOriginalContent(content);
      setShowUrdu(false);
      // Reset document direction
      document.documentElement.dir = 'ltr';
      document.documentElement.lang = 'en';
    } else {
      // Translate to Urdu
      handleTranslate();
      // Set document direction to RTL
      document.documentElement.dir = 'rtl';
      document.documentElement.lang = 'ur';
    }
  };

  // Apply RTL styling when showing Urdu content
  useEffect(() => {
    if (showUrdu) {
      document.documentElement.dir = 'rtl';
      document.documentElement.lang = 'ur';
    } else {
      document.documentElement.dir = 'ltr';
      document.documentElement.lang = 'en';
    }

    // Cleanup on unmount
    return () => {
      document.documentElement.dir = 'ltr';
      document.documentElement.lang = 'en';
    };
  }, [showUrdu]);

  return (
    <div>
      <button
        onClick={handleToggleLanguage}
        style={{
          padding: '0.5rem 1rem',
          backgroundColor: '#4285f4',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          marginBottom: '1rem',
          display: 'inline-block'
        }}
      >
        {showUrdu ? 'Back to English' : 'Translate to Urdu'}
      </button>

      {isLoading && (
        <div style={{ padding: '1rem', textAlign: 'center' }}>
          Translating to Urdu...
        </div>
      )}

      {error && (
        <div style={{
          padding: '1rem',
          backgroundColor: '#ffe6e6',
          color: 'red',
          borderRadius: '4px',
          marginBottom: '1rem'
        }}>
          Translation error: {error}
        </div>
      )}

      {showUrdu && !isLoading && !error && (
        <div
          style={{
            direction: 'rtl',
            textAlign: 'right',
            fontFamily: '"Jameel Noori Nastaleeq", "Urdu Typesetting", "Arial Unicode MS", sans-serif'
          }}
          dangerouslySetInnerHTML={{ __html: translatedContent || '' }}
        />
      )}

      {!showUrdu && (
        <div>{content}</div>
      )}
    </div>
  );
};

export default UrduTranslationComponent;