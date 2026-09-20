import React from 'react';
import { Home, FileText, Settings, History, ChevronLeft, ChevronRight } from 'lucide-react';

export default function Sidebar({ isOpen, toggleSidebar, activeView, setActiveView }) {
  const menuItems = [
    { id: 'dashboard', icon: <Home className="w-5 h-5" />, label: 'Dashboard' },
    { id: 'documents', icon: <FileText className="w-5 h-5" />, label: 'My Documents' },
    { id: 'recent', icon: <History className="w-5 h-5" />, label: 'Recent Analysis' },
    { id: 'settings', icon: <Settings className="w-5 h-5" />, label: 'Settings' },
  ];

  return (
    <aside 
      className={`bg-white border-r border-gray-200 transition-all duration-300 ease-in-out flex flex-col h-full ${
        isOpen ? 'w-64' : 'w-16'
      }`}
    >
      <div className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-2 px-2">
          {menuItems.map((item) => (
            <li key={item.id}>
              <button 
                onClick={() => setActiveView(item.id)}
                className={`w-full flex items-center px-3 py-3 rounded-lg group whitespace-nowrap transition-colors focus:outline-none ${
                  activeView === item.id 
                    ? 'bg-[#1a365d] text-white shadow-sm' 
                    : 'text-[#1a365d] hover:bg-gray-100 font-medium'
                }`}
                title={!isOpen ? item.label : undefined}
              >
                <div className="flex-shrink-0 flex items-center justify-center w-8">
                  {item.icon}
                </div>
                <span 
                  className={`ml-3 font-medium transition-opacity duration-300 text-left ${
                    isOpen ? 'opacity-100' : 'opacity-0 w-0 overflow-hidden'
                  }`}
                >
                  {item.label}
                </span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <div className="p-3 border-t border-gray-200 flex justify-end">
        <button 
          onClick={toggleSidebar}
          className="p-1.5 rounded-full hover:bg-gray-100 text-gray-600 focus:outline-none focus:ring-2 focus:ring-government-lightBlue"
          aria-label={isOpen ? "Collapse Sidebar" : "Expand Sidebar"}
        >
          {isOpen ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
        </button>
      </div>
    </aside>
  );
}
