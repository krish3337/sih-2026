import React, { useState } from 'react';
import { Bot, CheckCircle2, ChevronDown, Eye, FileText, Share2, Info, Loader2 } from 'lucide-react';

const StandardCard = ({ std }) => {
  const [expanded, setExpanded] = useState(false);

  // Match Confidence Badge
  let confLevel = "Medium";
  let confColor = "bg-green-50 text-green-600";
  if (std.low_confidence) {
    confLevel = "Low";
    confColor = "bg-yellow-50 text-yellow-600";
  } else if (std.similarity_score > 0.85) {
    confLevel = "High";
    confColor = "bg-green-100 text-green-700";
  }

  // Status Badge
  let statusText = std.status || "Status not verified";
  let statusColor = "bg-gray-100 text-gray-600";
  if (statusText === "Active" || statusText === "Current") {
    statusText = "Current";
    statusColor = "bg-blue-50 text-blue-700";
  } else if (statusText === "Superseded" || statusText === "Withdrawn") {
    if (std.superseding_is && std.superseding_is !== "N/A") {
      statusText = `Superseded (Replaced by ${std.superseding_is})`;
    }
    statusColor = "bg-red-50 text-red-700";
  }

  // Group Allied Standards
  const groupedAllied = {};
  if (std.allied_standards && std.allied_standards.length > 0) {
    std.allied_standards.forEach(a => {
      const type = a.relation_type || "Other related standards";
      if (!groupedAllied[type]) groupedAllied[type] = [];
      groupedAllied[type].push(a);
    });
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      {/* 1. Header (Always Visible) */}
      <div 
        className="p-4 cursor-pointer flex flex-col space-y-3 hover:bg-gray-50/50 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-start justify-between">
          <div className="flex items-start pr-4">
            <div className="h-10 w-10 bg-[#1a365d] rounded-lg text-white font-bold flex items-center justify-center shrink-0 mr-4 shadow-sm">
              IS
            </div>
            <div>
              <h3 className="font-bold text-[#1a365d] text-lg leading-tight">{std.standard_id}</h3>
              <p className="text-sm text-gray-600 mt-1">{std.title}</p>
            </div>
          </div>
          <div className="flex flex-col items-end space-y-2 shrink-0">
            <span className={`text-xs font-bold px-3 py-1 rounded-full ${confColor}`}>
              {confLevel} Match
            </span>
            <span className={`text-xs font-bold px-3 py-1 rounded-full ${statusColor}`}>
              {statusText}
            </span>
          </div>
        </div>

        {/* Compact Certification Badge (Always Visible) */}
        <div className="flex items-center justify-between mt-2 pt-3 border-t border-gray-100">
          <div className="flex items-center text-sm font-medium">
            {std.certification && std.certification.mandatory === "Yes" ? (
              <span className="text-red-600 flex items-center"><Info className="w-4 h-4 mr-1.5"/> Mandatory BIS Certification</span>
            ) : std.certification ? (
              <span className="text-green-600 flex items-center"><CheckCircle2 className="w-4 h-4 mr-1.5"/> Voluntary Certification</span>
            ) : (
              <span className="text-gray-500 flex items-center italic"><Info className="w-4 h-4 mr-1.5"/> Certification status not found - verify with BIS</span>
            )}
          </div>
          <button className="text-gray-400 hover:text-gray-600 transition-transform duration-200" style={{ transform: expanded ? 'rotate(180deg)' : '' }}>
            <ChevronDown className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Expanded Content */}
      {expanded && (
        <div className="px-5 pb-5 pt-3 border-t border-gray-100 bg-[#f8fafc] space-y-5">
          
          {/* 2. Version and Amendments */}
          <div>
            <h4 className="text-sm font-bold text-gray-700 mb-2 flex items-center">
              <span className="bg-gray-200 text-gray-600 text-[10px] uppercase px-2 py-0.5 rounded font-bold mr-2 tracking-wider">Status Register</span>
              Version & Amendments
            </h4>
            <div className="bg-white p-3.5 rounded-lg border border-gray-200 text-sm shadow-sm">
              <p className="text-gray-800 mb-2"><span className="font-semibold text-gray-500 w-24 inline-block">Latest Version:</span> {std.current_version_year}</p>
              <div className="text-gray-800">
                <span className="font-semibold text-gray-500 mb-1 block">Amendments: </span>
                {std.amendments && std.amendments.length > 0 ? (
                  <ul className="list-disc pl-5 mt-1 space-y-1.5 text-gray-600">
                    {std.amendments.map((amd, i) => (
                      <li key={i}>
                        <span className="font-medium text-gray-700">{amd.amendment_id || amd.amendment_number || `AMD-${i+1}`}</span>
                        {amd.date_issued ? ` (${amd.date_issued})` : ''} - {amd.summary_of_change || amd.description || 'No description provided'}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <span className="text-gray-500 italic">No amendments recorded</span>
                )}
              </div>
            </div>
          </div>

          {/* 5. Certification Block */}
          <div>
            <h4 className="text-sm font-bold text-gray-700 mb-2 flex items-center">
              <span className="bg-gray-200 text-gray-600 text-[10px] uppercase px-2 py-0.5 rounded font-bold mr-2 tracking-wider">Certification Register</span>
              Certification Details
            </h4>
            <div className="bg-white p-3.5 rounded-lg border border-gray-200 text-sm shadow-sm">
              {std.certification ? (
                <div className="space-y-2">
                  <p><span className="font-semibold text-gray-500 w-28 inline-block">Scheme:</span> <span className="text-gray-800">{std.certification.certification_name || "BIS Product Certification"}</span></p>
                  <p><span className="font-semibold text-gray-500 w-28 inline-block">Status:</span> <span className={std.certification.mandatory === "Yes" ? "text-red-600 font-medium" : "text-green-600 font-medium"}>{std.certification.mandatory === "Yes" ? "Mandatory" : "Voluntary"}</span></p>
                  {std.certification.qco_reference && (
                    <p><span className="font-semibold text-gray-500 w-28 inline-block">QCO Reference:</span> <span className="text-gray-800">{std.certification.qco_reference}</span></p>
                  )}
                </div>
              ) : (
                <p className="text-gray-500 italic">Certification status not found in register - verify with BIS.</p>
              )}
            </div>
          </div>

          {/* 4. Allied Standards */}
          {Object.keys(groupedAllied).length > 0 && (
            <div>
              <h4 className="text-sm font-bold text-gray-700 mb-2">Allied Standards</h4>
              <div className="space-y-3">
                {Object.entries(groupedAllied).map(([groupName, items]) => (
                  <div key={groupName} className="bg-white p-3.5 rounded-lg border border-gray-200 shadow-sm">
                    <p className="text-[11px] font-bold text-[#2b6cb0] uppercase mb-2 tracking-wider">{groupName}</p>
                    <ul className="space-y-2">
                      {items.map((item, i) => (
                        <li key={i} className="text-sm text-gray-600 flex items-start leading-snug">
                          <span className="text-[#2b6cb0] mr-2 mt-0.5">•</span>
                          <span><strong className="text-gray-800 font-semibold">{item.standard_id}</strong> - {item.title}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>
      )}

      {/* 6. Footer Actions (Always Visible) */}
      <div className="bg-white border-t border-gray-100 px-4 py-3 flex items-center justify-end space-x-3 rounded-b-xl">
        <button className="flex items-center text-sm font-medium text-[#1a365d] hover:bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-200 transition-colors">
          <Eye className="w-4 h-4 mr-2" />
          View Evidence
        </button>
        <button className="flex items-center text-sm font-medium text-white bg-[#1a365d] hover:bg-[#122847] px-4 py-1.5 rounded-lg transition-colors shadow-sm">
          <FileText className="w-4 h-4 mr-2" />
          View Full Standard
        </button>
      </div>
      
    </div>
  );
};

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
        {status === 'completed' && results && (() => {
          const hasLowConfidence = results.warnings?.some(w => w.code === 'NO_CONFIDENT_MATCH') || 
                                   (results.recommendations?.length > 0 && results.recommendations[0].low_confidence);
          
          return (
          <div className="p-5 space-y-5 animate-fade-in-up">
            
            {/* Low Confidence Warning */}
            {hasLowConfidence && (
              <div className="bg-orange-50 border border-orange-200 p-6 rounded-xl text-center mb-2 shadow-sm">
                <div className="h-12 w-12 bg-orange-100 text-orange-600 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Info className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-bold text-orange-800 mb-2">No Relevant Standards Found</h3>
                <p className="text-orange-700 text-sm">
                  We couldn't find any highly confident matches for your query. 
                  The results below are shown as best-effort guesses but may not be relevant.
                </p>
              </div>
            )}

            {/* Explanation box */}
            {results.explanation && (
              <div className="bg-blue-50 border border-blue-100 p-4 rounded-xl text-sm text-[#1a365d] mb-4">
                <strong>AI Explanation:</strong> {results.explanation}
              </div>
            )}

            {(results.recommendations || []).map((std, idx) => (
              <StandardCard key={idx} std={std} />
            ))}
          </div>
          );
        })()}
      </div>
    </div>
  );
}
