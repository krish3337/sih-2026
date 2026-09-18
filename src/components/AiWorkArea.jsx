import React from 'react';
import { Bot, CheckCircle2, ChevronDown, Eye, FileText, Share2, Info, Loader2 } from 'lucide-react';

export default function AiWorkArea({ status = 'idle' }) {
  // Using the exact data from the mockup
  const extractedStandards = [
    { 
      id: 'IS 302 : 2019', 
      title: 'Safety of Household Electrical Appliances',
      relevance: 94,
      clauses: [
        'Clause 8.1 — Protection against electric shock',
        'Clause 15.2 — Moisture resistance',
        'Clause 22.4 — Insulation requirements'
      ],
      source: 'Page 18, Clause 8.1'
    },
    { 
      id: 'IS 13420 : 2021', 
      title: 'Household and Similar Electrical Appliances — Safety',
      relevance: 78,
      clauses: [
        'Clause 6.1 — Mechanical strength',
        'Clause 9.3 — Temperature rise limits'
      ],
      source: 'Page 12, Clause 6.1'
    },
    { 
      id: 'IS 10322 : 2012', 
      title: 'Electromagnetic Compatibility',
      relevance: 62,
      clauses: [
        'Clause 5.2 — Emission limits',
        'Clause 7.1 — Immunity requirements'
      ],
      source: 'Page 27, Clause 5.2'
    }
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 h-full flex flex-col overflow-hidden">
      
      {/* Header */}
      <div className="flex items-center justify-between p-5 border-b border-gray-100 bg-white">
        <div className="flex items-center">
          <Bot className="h-6 w-6 text-[#1a365d] mr-2" />
          <h2 className="text-lg font-bold text-[#1a365d]">AI Analysis & Extracted Standards</h2>
        </div>
        {status === 'completed' && (
          <div className="flex items-center text-xs font-bold text-green-700 bg-green-50 px-3 py-1.5 rounded-full border border-green-200 animate-fade-in">
            <CheckCircle2 className="w-4 h-4 mr-1.5" />
            3 Relevant Standards Found
          </div>
        )}
      </div>

      {/* Content Scrollable Area */}
      <div className="flex-1 overflow-y-auto bg-[#f8fafc] relative">
        
        {/* State: IDLE */}
        {status === 'idle' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center p-8 text-gray-400">
            <div className="h-20 w-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <Info className="h-10 w-10 text-gray-300" />
            </div>
            <p className="text-center font-medium text-gray-500 mb-2">Awaiting Document Upload</p>
            <p className="text-center text-sm">
              Upload a product standard PDF to begin the AI-powered extraction process.
            </p>
          </div>
        )}

        {/* State: PROCESSING */}
        {status === 'processing' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center p-8">
            <div className="relative mb-6">
              <div className="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
              <div className="absolute inset-0 border-4 border-[#1a365d] rounded-full border-t-transparent animate-spin"></div>
              <Bot className="h-10 w-10 text-[#1a365d] m-6 animate-pulse" />
            </div>
            <p className="text-lg font-bold text-[#1a365d] mb-1">Analyzing Document...</p>
            <p className="text-sm text-gray-500 text-center">
              Extracting clauses and cross-referencing with the Government Indian Standards database.
            </p>
          </div>
        )}

        {/* State: COMPLETED */}
        {status === 'completed' && (
          <div className="p-5 space-y-5 animate-fade-in-up">
            {extractedStandards.map((std, idx) => (
              <div key={idx} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                
                {/* Standard Header */}
                <div className="p-4 flex items-start justify-between">
                  <div className="flex items-start">
                    <div className="h-10 w-10 bg-[#1a365d] rounded-lg text-white font-bold flex items-center justify-center shrink-0 mr-4 shadow-sm">
                      IS
                    </div>
                    <div>
                      <h3 className="font-bold text-[#1a365d] text-lg leading-tight">{std.id}</h3>
                      <p className="text-sm text-gray-500 mt-0.5">{std.title}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                      std.relevance >= 90 ? 'bg-green-100 text-green-700' : 
                      std.relevance >= 75 ? 'bg-green-50 text-green-600' : 'bg-yellow-50 text-yellow-600'
                    }`}>
                      Relevance {std.relevance}%
                    </span>
                    <button className="text-gray-400 hover:text-gray-600">
                      <ChevronDown className="w-5 h-5" />
                    </button>
                  </div>
                </div>
                
                {/* Clauses */}
                <div className="px-14 pb-4">
                  <p className="text-sm font-bold text-gray-700 mb-2">Relevant Clauses</p>
                  <ul className="list-disc pl-4 space-y-1">
                    {std.clauses.map((clause, cIdx) => (
                      <li key={cIdx} className="text-sm text-gray-600">{clause}</li>
                    ))}
                  </ul>
                </div>

                {/* Footer Actions */}
                <div className="bg-[#f8fafc] border-t border-gray-100 px-4 py-3 flex items-center justify-between">
                  <div className="flex items-center text-sm text-[#2b6cb0] font-medium">
                    <Share2 className="w-4 h-4 mr-2 text-[#2b6cb0]" />
                    Source: {std.source}
                  </div>
                  <div className="flex space-x-3">
                    <button className="flex items-center text-sm font-medium text-[#1a365d] hover:bg-gray-100 px-3 py-1.5 rounded-lg border border-transparent transition-colors">
                      <Eye className="w-4 h-4 mr-2" />
                      View Evidence
                    </button>
                    <button className="flex items-center text-sm font-medium text-[#1a365d] bg-white border border-gray-200 hover:border-[#1a365d] px-3 py-1.5 rounded-lg transition-colors shadow-sm">
                      <FileText className="w-4 h-4 mr-2" />
                      View Full Standard
                    </button>
                  </div>
                </div>
                
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
