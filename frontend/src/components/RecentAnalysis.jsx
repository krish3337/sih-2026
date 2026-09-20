import React from 'react';
import { History, FileText, Search, ExternalLink } from 'lucide-react';

export default function RecentAnalysis() {
  const recentTasks = [
    { id: 'ANL-9021', date: '2026-09-15', docName: 'Steel_Bars_Specs.pdf', status: 'Completed', query: 'What are the tensile strength standards?' },
    { id: 'ANL-9020', date: '2026-09-14', docName: 'Cement_Quality_Control.pdf', status: 'Completed', query: 'List all relevant IS codes for Portland Cement.' },
    { id: 'ANL-9019', date: '2026-09-12', docName: 'Electrical_Cables_Draft.pdf', status: 'Pending Review', query: 'Extract insulation thickness standards.' },
    { id: 'ANL-9018', date: '2026-09-10', docName: 'Water_Pipes_Schedule.pdf', status: 'Completed', query: 'Identify pressure testing requirements.' },
  ];

  return (
    <div className="card h-full flex flex-col">
      <div className="flex items-center justify-between mb-6 border-b border-gray-200 pb-4">
        <div className="flex items-center">
          <History className="h-8 w-8 text-government-blue mr-3" />
          <h1 className="text-2xl font-bold text-government-blue">Recent Analysis</h1>
        </div>
        
        <div className="relative">
          <input 
            type="text" 
            placeholder="Search recent work..." 
            className="input-field pl-10 py-1.5 text-sm w-64"
          />
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
        </div>
      </div>

      <div className="flex-1 overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Analysis ID</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source Document</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User Query</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" className="relative px-6 py-3"><span className="sr-only">Actions</span></th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {recentTasks.map((task) => (
              <tr key={task.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-government-blue">{task.id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{task.date}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 flex items-center">
                  <FileText className="w-4 h-4 mr-2 text-gray-400" />
                  {task.docName}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">{task.query}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    task.status === 'Completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {task.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-government-lightBlue hover:text-government-blue flex items-center justify-end w-full">
                    View <ExternalLink className="w-3 h-3 ml-1" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {recentTasks.length === 0 && (
          <div className="text-center py-10 text-gray-500">
            No recent analysis found.
          </div>
        )}
      </div>
    </div>
  );
}
