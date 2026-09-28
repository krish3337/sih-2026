import React, { useState } from 'react';
import PdfUpload from './PdfUpload';
import MultilingualInput from './MultilingualInput';
import AiWorkArea from './AiWorkArea';
import WelcomeBanner from './WelcomeBanner';

export default function HomeDashboard() {
  const [analysisStatus, setAnalysisStatus] = useState('idle'); // 'idle', 'processing', 'completed', 'error'
  const [results, setResults] = useState(null);

  const handleFileUpload = async (file) => {
    if (file) {
      setAnalysisStatus('processing');
      try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('http://localhost:8000/v1/recommend/pdf', {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        setResults(data);
        setAnalysisStatus('completed');
      } catch (err) {
        console.error(err);
        setAnalysisStatus('error');
      }
    } else {
      setAnalysisStatus('idle');
      setResults(null);
    }
  };

  const handleTextSubmit = async (text, language) => {
    if (!text) return;
    setAnalysisStatus('processing');
    try {
      const response = await fetch('http://localhost:8000/v1/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, language_hint: language }),
      });
      
      if (!response.ok) throw new Error('API Error');
      const data = await response.json();
      
      setResults(data);
      setAnalysisStatus('completed');
    } catch (err) {
      console.error(err);
      setAnalysisStatus('error');
    }
  };

  return (
    <div className="flex flex-col h-full">
      <WelcomeBanner />
      
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 flex-1 min-h-[500px]">
        {/* Left Column: Upload and Input */}
        <div className="xl:col-span-5 flex flex-col space-y-6">
          <PdfUpload onUpload={handleFileUpload} />
          <MultilingualInput onSubmit={handleTextSubmit} />
        </div>
        
        {/* Right Column: AI Work Area */}
        <div className="xl:col-span-7 relative h-[600px] xl:h-auto">
          <div className="h-full xl:absolute xl:inset-0">
            <AiWorkArea status={analysisStatus} results={results} />
          </div>
        </div>
      </div>
    </div>
  );
}
