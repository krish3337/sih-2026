import React from 'react';
import { FolderOpen, File, MoreVertical, Download } from 'lucide-react';

export default function MyDocuments() {
  const documents = [
    { id: 'DOC-001', name: 'Steel_Bars_Specs.pdf', uploadDate: '2026-09-15', size: '2.4 MB', processed: true },
    { id: 'DOC-002', name: 'Cement_Quality_Control.pdf', uploadDate: '2026-09-14', size: '1.1 MB', processed: true },
    { id: 'DOC-003', name: 'Electrical_Cables_Draft.pdf', uploadDate: '2026-09-12', size: '4.5 MB', processed: true },
    { id: 'DOC-004', name: 'Water_Pipes_Schedule.pdf', uploadDate: '2026-09-10', size: '0.8 MB', processed: true },
    { id: 'DOC-005', name: 'Highway_Lighting_Poles.pdf', uploadDate: '2026-09-08', size: '3.2 MB', processed: false },
    { id: 'DOC-006', name: 'Safety_Valves_Specs.pdf', uploadDate: '2026-09-05', size: '1.5 MB', processed: true },
  ];

  return (
    <div className="card h-full flex flex-col">
      <div className="flex items-center justify-between mb-6 border-b border-gray-200 pb-4">
        <div className="flex items-center">
          <FolderOpen className="h-8 w-8 text-government-blue mr-3" />
          <h1 className="text-2xl font-bold text-government-blue">My Documents</h1>
        </div>
        <button className="btn-primary text-sm">
          Upload New Document
        </button>
      </div>

      <div className="flex-1 overflow-y-auto pr-2">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {documents.map((doc) => (
            <div key={doc.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow bg-white flex flex-col">
              <div className="flex justify-between items-start mb-3">
                <div className="bg-blue-50 p-2 rounded-lg">
                  <File className="w-6 h-6 text-government-lightBlue" />
                </div>
                <button className="text-gray-400 hover:text-gray-600 focus:outline-none">
                  <MoreVertical className="w-5 h-5" />
                </button>
              </div>
              
              <h3 className="font-medium text-gray-900 truncate mb-1" title={doc.name}>
                {doc.name}
              </h3>
              
              <div className="flex justify-between items-center text-xs text-gray-500 mb-4">
                <span>{doc.size}</span>
                <span>Uploaded: {doc.uploadDate}</span>
              </div>
              
              <div className="mt-auto flex justify-between items-center pt-3 border-t border-gray-100">
                <span className={`text-xs px-2 py-1 rounded-full ${
                  doc.processed ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                }`}>
                  {doc.processed ? 'Processed' : 'Unprocessed'}
                </span>
                
                <button className="text-government-lightBlue hover:text-government-blue focus:outline-none" title="Download Document">
                  <Download className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
