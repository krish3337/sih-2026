import React, { useState } from 'react';
import { Send, Languages } from 'lucide-react';

export default function MultilingualInput({ onSubmit }) {
  const [language, setLanguage] = useState('en');
  const [text, setText] = useState('');
  const maxLength = 500;

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'Hindi (हिन्दी)' },
    { code: 'bn', name: 'Bengali (বাংলা)' },
    { code: 'te', name: 'Telugu (తెలుగు)' },
    { code: 'mr', name: 'Marathi (मराठी)' },
    { code: 'ta', name: 'Tamil (தமிழ்)' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    if (onSubmit) onSubmit(text, language);
  };

  const handleTextChange = (e) => {
    const newText = e.target.value;
    if (newText.length <= maxLength) {
      setText(newText);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col">
      <div className="flex items-center mb-4">
        <h2 className="text-lg font-bold text-[#1a365d] flex items-center">
          <Languages className="w-5 h-5 mr-2 text-[#2b6cb0]" />
          Enter your query (any language)
        </h2>
      </div>
      
      <form onSubmit={handleSubmit} className="flex flex-col">
        <div className="relative mb-4">
          <textarea
            value={text}
            onChange={handleTextChange}
            placeholder="Enter your query or additional context here..."
            className="w-full border border-gray-300 rounded-xl px-4 py-3 pb-8 text-sm focus:outline-none focus:ring-1 focus:ring-[#1a365d] focus:border-[#1a365d] min-h-[120px] resize-none"
            dir={language === 'ur' ? 'rtl' : 'ltr'}
          ></textarea>
          <div className="absolute bottom-3 right-4 text-xs text-gray-400 font-medium">
            {text.length}/{maxLength}
          </div>
        </div>
        
        <div className="flex justify-end">
          <button 
            type="submit" 
            className="bg-[#1a365d] hover:bg-[#122847] text-white px-6 py-2 rounded-lg flex items-center font-medium transition-colors text-sm shadow-sm"
            disabled={!text.trim()}
          >
            <Send className="w-4 h-4 mr-2" />
            Submit Query
          </button>
        </div>
      </form>
    </div>
  );
}
