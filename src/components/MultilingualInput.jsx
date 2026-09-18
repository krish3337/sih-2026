import React, { useState } from 'react';
import { Send, Languages } from 'lucide-react';

export default function MultilingualInput() {
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
    console.log(`Submitted in ${language}: ${text}`);
    setText('');
  };

  const handleTextChange = (e) => {
    const newText = e.target.value;
    if (newText.length <= maxLength) {
      setText(newText);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-[#1a365d] flex items-center">
          <Languages className="w-5 h-5 mr-2 text-[#2b6cb0]" />
          Multilingual Query
        </h2>
        <div className="flex items-center">
          <label htmlFor="language-select" className="text-sm text-gray-500 mr-3">Input Language:</label>
          <div className="relative">
            <select 
              id="language-select"
              value={language} 
              onChange={(e) => setLanguage(e.target.value)}
              className="appearance-none border border-gray-300 rounded-lg px-3 py-1.5 pr-8 text-sm text-gray-700 bg-white focus:outline-none focus:ring-1 focus:ring-[#1a365d] focus:border-[#1a365d]"
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
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
