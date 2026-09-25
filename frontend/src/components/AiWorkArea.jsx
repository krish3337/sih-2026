import React from 'react';
import { Bot, CheckCircle2, ChevronDown, Eye, FileText, Share2, Info, Loader2 } from 'lucide-react';

export default function AiWorkArea({ status = 'idle', results }) {
  // Render the AI work area
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 h-full flex flex-col overflow-hidden">
      
      {/* Header */}
      <div className="flex items-center justify-between p-5 border-b border-gray-100 bg-white">
        <div className="flex items-center">
          <Bot className="h-6 w-6 text-[#1a365d] mr-2" />
          <h2 className="text-lg font-bold text-[#1a365d]">AI Analysis & Extracted Standards</h2>
        </div>
        {status === 'completed' && results && (
          <div className="flex items-center text-xs font-bold text-green-700 bg-green-50 px-3 py-1.5 rounded-full border border-green-200 animate-fade-in">
            <CheckCircle2 className="w-4 h-4 mr-1.5" />
            {results.recommendations?.length || 0} Relevant Standards Found
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

        {/* State: ERROR */}
        {status === 'error' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center p-8 text-red-500">
            <div className="h-20 w-20 bg-red-100 rounded-full flex items-center justify-center mb-4">
              <Info className="h-10 w-10 text-red-500" />
            </div>
            <p className="text-center font-bold mb-2">Error Processing Request</p>
            <p className="text-center text-sm text-red-400">
              There was an error communicating with the AI API. Make sure the backend server is running.
            </p>
          </div>
        )}

        {/* State: COMPLETED */}
        {status === 'completed' && results && (
          <div className="p-5 space-y-5 animate-fade-in-up">
            
            {/* Explanation box */}
            {results.explanation && (
              <div className="bg-blue-50 border border-blue-100 p-4 rounded-xl text-sm text-[#1a365d] mb-4">
                <strong>AI Explanation:</strong> {results.explanation}
              </div>
            )}

            {(results.recommendations || []).map((std, idx) => {
              const relevanceScore = Math.round((std.similarity_score || 0) * 100);
              return (
              <div key={idx} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                
                {/* Standard Header */}
                <div className="p-4 flex items-start justify-between">
                  <div className="flex items-start">
                    <div className="h-10 w-10 bg-[#1a365d] rounded-lg text-white font-bold flex items-center justify-center shrink-0 mr-4 shadow-sm">
                      IS
                    </div>
                    <div>
                      <h3 className="font-bold text-[#1a365d] text-lg leading-tight">{std.standard_id}</h3>
                      <p className="text-sm text-gray-500 mt-0.5">{std.title}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                      relevanceScore >= 90 ? 'bg-green-100 text-green-700' : 
                      relevanceScore >= 75 ? 'bg-green-50 text-green-600' : 'bg-yellow-50 text-yellow-600'
                    }`}>
                      Relevance {relevanceScore}%
                    </span>
                    <button className="text-gray-400 hover:text-gray-600">
                      <ChevronDown className="w-5 h-5" />
                    </button>
                  </div>
                </div>
                
                {/* Allied Standards */}
                <div className="px-14 pb-4">
                  {results.allied_standards && results.allied_standards.length > 0 ? (
                    <>
                      <p className="text-sm font-bold text-gray-700 mb-2">Allied Standards</p>
                      <ul className="list-disc pl-4 space-y-1">
                        {results.allied_standards.slice(0, 5).map((related, rIdx) => (
                          <li key={rIdx} className="text-sm text-gray-600">{related.standard_id} - {related.relation_type}</li>
                        ))}
                      </ul>
                    </>
                  ) : (
                    <p className="text-sm text-gray-500 italic">No allied standards found.</p>
                  )}
                </div>

                {/* Footer Actions */}
                <div className="bg-[#f8fafc] border-t border-gray-100 px-4 py-3 flex items-center justify-between">
                  <div className="flex items-center text-sm text-[#2b6cb0] font-medium">
                    {std.certification?.mandatory ? (
                      <span className="text-red-600">⚠ Mandatory BIS Certification</span>
                    ) : (
                      <span className="text-green-600">✓ Voluntary</span>
                    )}
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
            )})}
          </div>
        )}
      </div>
    </div>
  );
}
