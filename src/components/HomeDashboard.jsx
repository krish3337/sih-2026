import React, { useState } from 'react';
import PdfUpload from './PdfUpload';
import MultilingualInput from './MultilingualInput';
import AiWorkArea from './AiWorkArea';
import WelcomeBanner from './WelcomeBanner';

export default function HomeDashboard() {
  const [analysisStatus, setAnalysisStatus] = useState('idle'); // 'idle', 'processing', 'completed'

  const handleFileUpload = (file) => {
    if (file) {
      setAnalysisStatus('processing');
      
      // Simulate AI processing time (3 seconds) before showing results
      setTimeout(() => {
        setAnalysisStatus('completed');
      }, 3000);
    } else {
      setAnalysisStatus('idle');
    }
  };

  return (
    <div className="flex flex-col h-full">
      <WelcomeBanner />
      
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 flex-1 min-h-[500px]">
        {/* Left Column: Upload and Input */}
        <div className="xl:col-span-5 flex flex-col space-y-6">
          <PdfUpload onUpload={handleFileUpload} />
          <MultilingualInput />
        </div>
        
        {/* Right Column: AI Work Area */}
        <div className="xl:col-span-7 h-full">
          <AiWorkArea status={analysisStatus} />
        </div>
      </div>
    </div>
  );
}
