import { useState } from 'react';
import { UploadCloud, FileText, Type } from 'lucide-react';

export default function Home({ onAnalyze, onAnalyzeSelected }) {
  const [activeTab, setActiveTab] = useState('text');
  const [manualText, setManualText] = useState('');
  const [pdfFile, setPdfFile] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
    } else {
      alert("Please upload a valid PDF file.");
    }
  };

  return (
    <div className="flex flex-col flex-1 p-5 overflow-y-auto">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-slate-800">Analyze Specification</h2>
        <p className="text-sm text-slate-500 mt-1">Select text or upload a document.</p>
      </div>

      <div className="flex bg-slate-200 p-1 rounded-md mb-4">
        <button
          onClick={() => setActiveTab('text')}
          className={`flex-1 flex items-center justify-center space-x-2 py-1.5 text-sm font-medium rounded transition-colors ${activeTab === 'text' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-600 hover:text-slate-800'}`}
        >
          <Type className="w-4 h-4" />
          <span>Text Input</span>
        </button>
        <button
          onClick={() => setActiveTab('pdf')}
          className={`flex-1 flex items-center justify-center space-x-2 py-1.5 text-sm font-medium rounded transition-colors ${activeTab === 'pdf' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-600 hover:text-slate-800'}`}
        >
          <FileText className="w-4 h-4" />
          <span>PDF Upload</span>
        </button>
      </div>

      {activeTab === 'text' && (
        <div className="flex-1 flex flex-col min-h-0 mb-4 animate-in fade-in slide-in-from-left-2 duration-300">
          <textarea
            className="flex-1 w-full p-3 border border-slate-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm resize-none min-h-[120px]"
            placeholder="Paste procurement specification here..."
            value={manualText}
            onChange={(e) => setManualText(e.target.value)}
          />
          <div className="mt-4 flex flex-col space-y-3">
            <button
              onClick={() => onAnalyze({ type: 'text', content: manualText })}
              disabled={!manualText.trim()}
              className="w-full py-2.5 bg-blue-700 hover:bg-blue-800 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-medium rounded shadow-sm transition-colors"
            >
              Analyze Standards
            </button>
            <button
              onClick={onAnalyzeSelected}
              className="w-full py-2.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-medium rounded shadow-sm transition-colors"
            >
              Analyze Selected Text
            </button>
          </div>
        </div>
      )}

      {activeTab === 'pdf' && (
        <div className="flex-1 flex flex-col min-h-0 mb-4 animate-in fade-in slide-in-from-right-2 duration-300">
          <label className="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-slate-300 rounded-md bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer p-6 min-h-[120px]">
            <UploadCloud className="w-10 h-10 text-slate-400 mb-2" />
            <span className="text-sm font-medium text-slate-700">
              {pdfFile ? pdfFile.name : "Click to select PDF file"}
            </span>
            <span className="text-xs text-slate-500 mt-1">Max size: 25 MB</span>
            <input 
              type="file" 
              accept="application/pdf" 
              className="hidden" 
              onChange={handleFileChange}
            />
          </label>

          <div className="mt-4 flex flex-col space-y-3">
            <button
              onClick={() => onAnalyze({ type: 'pdf', content: pdfFile })}
              disabled={!pdfFile}
              className="w-full py-2.5 bg-blue-700 hover:bg-blue-800 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-medium rounded shadow-sm transition-colors"
            >
              Analyze PDF Document
            </button>
          </div>
        </div>
      )}

      {activeTab === 'text' && (
        <div className="mt-auto p-3 bg-blue-50 text-blue-800 rounded text-xs border border-blue-100 flex items-start">
          <span className="font-semibold mr-1">Tip:</span>
          <span>Select text on a tender webpage and use the extension.</span>
        </div>
      )}
    </div>
  );
}
