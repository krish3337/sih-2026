import React from 'react';
import { ChevronRight } from 'lucide-react';

export default function WelcomeBanner() {
  const steps = [
    { number: 1, title: 'Upload Document', desc: 'Add your product PDF' },
    { number: 2, title: 'Ask Query', desc: 'In English or Indian language' },
    { number: 3, title: 'AI Analysis', desc: 'Processes the document' },
    { number: 4, title: 'Review Standards', desc: 'View relevant IS details' },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-[#1a365d] mb-1">Welcome to Indian Standards Extractor</h2>
          <p className="text-[#2b6cb0] font-medium">know latest indian standards relatedto the object</p>
        </div>
        <div className="hidden md:flex items-center text-sm font-bold text-[#1a365d] text-right mt-4 md:mt-0">
          <div className="leading-tight mr-3">
            <p>Better Standards</p>
            <p>Safer Tomorrow</p>
          </div>
          {/* Decorative tricolor graphic to represent the emblem area in the mock */}
          <div className="h-10 w-12 flex flex-col justify-center gap-1 opacity-80">
             <div className="h-1.5 w-full bg-[#FF9933] rounded-full transform rotate-12"></div>
             <div className="h-1.5 w-full bg-gray-300 rounded-full"></div>
             <div className="h-1.5 w-full bg-[#138808] rounded-full transform -rotate-12"></div>
          </div>
        </div>
      </div>

      <div className="flex flex-col md:flex-row items-center justify-between bg-[#f8fafc] rounded-lg p-4 px-6">
        {steps.map((step, index) => (
          <React.Fragment key={index}>
            <div className="flex items-center space-x-3 w-full md:w-auto my-2 md:my-0">
              <div className="h-8 w-8 rounded-full bg-[#1a365d] text-white flex items-center justify-center font-bold text-sm shrink-0">
                {step.number}
              </div>
              <div className="flex flex-col">
                <span className="text-[#1a365d] font-bold text-sm leading-tight">{step.title}</span>
                <span className="text-gray-500 text-xs">{step.desc}</span>
              </div>
            </div>
            {index < steps.length - 1 && (
              <ChevronRight className="hidden md:block w-5 h-5 text-gray-400 mx-2 shrink-0" />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
