import React, { useState } from 'react';
import { UploadCloud, CheckCircle2, Trash2, CheckCircle } from 'lucide-react';

export default function PdfUpload({ onUpload }) {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelection(e.target.files[0]);
    }
  };

  const handleFileSelection = (selectedFile) => {
    if (selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      if (onUpload) onUpload(selectedFile);
    } else {
      alert('Please upload a valid PDF document.');
    }
  };

  const clearFile = () => {
    setFile(null);
    if (onUpload) onUpload(null);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col">
      <div className="flex items-center mb-4">
        <UploadCloud className="h-6 w-6 text-[#1a365d] mr-2" />
        <div>
          <h2 className="text-lg font-bold text-[#1a365d] leading-tight">Document Upload</h2>
          <p className="text-xs text-gray-500">Upload your product standard PDF to begin analysis.</p>
        </div>
      </div>
      
      <div 
        className={`relative flex flex-col items-center justify-center border-2 border-dashed rounded-xl p-8 mb-4 transition-colors ${
          isDragging ? 'border-[#1a365d] bg-blue-50' : 'border-[#cbd5e1] bg-white hover:bg-gray-50'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <UploadCloud className="h-10 w-10 text-gray-400 mb-3" />
        <p className="text-sm text-gray-700 text-center font-medium mb-1">
          Drag and drop your PDF here
        </p>
        <p className="text-sm text-gray-500 mb-4">or</p>
        
        <label className="bg-[#1a365d] hover:bg-[#122847] text-white px-6 py-2 rounded-lg cursor-pointer font-medium transition-colors text-sm mb-4">
          Browse Files
          <input 
            type="file" 
            className="hidden" 
            accept="application/pdf"
            onChange={handleFileInput}
          />
        </label>
        <p className="text-xs text-gray-400">Supported format: PDF <span className="mx-1">|</span> Max size: 25 MB</p>
      </div>

      {file && (
        <div className="flex items-center justify-between border border-green-200 bg-green-50/30 rounded-lg p-3 mb-4">
          <div className="flex items-center">
            <div className="h-10 w-10 bg-red-500 rounded flex items-center justify-center text-white font-bold text-xs mr-3">
              PDF
            </div>
            <div>
              <p className="text-sm font-bold text-gray-800 truncate max-w-[200px] sm:max-w-[300px]">{file.name}</p>
              <p className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(1)} MB</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="flex items-center text-xs font-bold text-green-700 bg-green-100 px-3 py-1 rounded-full">
              <CheckCircle2 className="w-3.5 h-3.5 mr-1" />
              Ready
            </span>
            <button 
              className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded transition-colors"
              onClick={clearFile}
              title="Remove file"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Trust Badges matching the image */}
      <div className="flex flex-col sm:flex-row justify-between items-center bg-green-50/50 rounded-lg p-2.5 px-4 mt-auto">
        <div className="flex items-center text-xs font-medium text-green-800">
          <CheckCircle className="w-3.5 h-3.5 mr-1.5 text-green-600" />
          Secure document processing
        </div>
        <div className="flex items-center text-xs font-medium text-green-800">
          <CheckCircle className="w-3.5 h-3.5 mr-1.5 text-green-600" />
          AI-powered analysis
        </div>
        <div className="flex items-center text-xs font-medium text-green-800">
          <CheckCircle className="w-3.5 h-3.5 mr-1.5 text-green-600" />
          Government standards database
        </div>
      </div>
    </div>
  );
}
