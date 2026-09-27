import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import HomeDashboard from './components/HomeDashboard';
import RecentAnalysis from './components/RecentAnalysis';
import MyDocuments from './components/MyDocuments';
import SplashScreen from './components/SplashScreen';
import { Shield, FileText, Languages, Lock, Users } from 'lucide-react';
import './index.css';

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [activeView, setActiveView] = useState('dashboard');

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const renderActiveView = () => {
    switch (activeView) {
      case 'dashboard':
        return <HomeDashboard />;
      case 'recent':
        return <RecentAnalysis />;
      case 'documents':
        return <MyDocuments />;
      default:
        return <HomeDashboard />;
    }
  };

  if (showSplash) {
    return <SplashScreen onComplete={() => setShowSplash(false)} />;
  }

  return (
    <div className="h-screen flex flex-col bg-gray-100 font-sans overflow-hidden">
      <Header />
      
      <div className="flex flex-1 overflow-hidden h-[calc(100vh-5rem)]">
        {/* Sidebar */}
        <Sidebar 
          isOpen={isSidebarOpen} 
          toggleSidebar={toggleSidebar} 
          activeView={activeView}
          setActiveView={setActiveView}
        />
        
        {/* Main Content Area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <main className="flex-1 overflow-y-auto w-full flex flex-col">
            <div className="flex-1 px-4 sm:px-6 lg:px-8 pt-4 pb-8">
              {renderActiveView()}
            </div>
            
            {/* Footer matches the image perfectly */}
            <footer className="bg-white border-t border-gray-200 py-6 px-8 text-xs text-gray-500 flex flex-col xl:flex-row justify-between items-start xl:items-center shrink-0">
              <div className="flex items-start mb-4 xl:mb-0 max-w-sm">
                <Shield className="w-8 h-8 text-government-blue mr-3 flex-shrink-0" />
                <div>
                  <p className="font-semibold text-government-blue mb-1">About this platform</p>
                  <p>This platform uses AI-assisted document analysis to help identify relevant Indian Standards from product documentation.</p>
                </div>
              </div>
              
              <div className="flex-1 xl:flex-none flex flex-col items-center mb-4 xl:mb-0 w-full xl:w-auto px-4">
                <p className="font-semibold text-government-blue mb-3 self-start xl:self-center">Trust & Governance</p>
                <div className="flex flex-wrap gap-x-6 gap-y-2 justify-start xl:justify-center">
                  <span className="flex items-center"><FileText className="w-3.5 h-3.5 mr-1.5" /> Source-grounded extraction</span>
                  <span className="flex items-center"><FileText className="w-3.5 h-3.5 mr-1.5" /> Clause-level references</span>
                  <span className="flex items-center"><Languages className="w-3.5 h-3.5 mr-1.5" /> Multilingual queries</span>
                  <span className="flex items-center"><Lock className="w-3.5 h-3.5 mr-1.5" /> Secure processing</span>
                  <span className="flex items-center"><Users className="w-3.5 h-3.5 mr-1.5" /> Human review supported</span>
                </div>
              </div>
              
              <div className="flex flex-col items-start xl:items-end w-full xl:w-auto">
                <p className="mb-2">Last updated: September 2026</p>
                <div className="flex space-x-4 text-government-blue">
                  <a href="#" className="hover:underline">Privacy & Security</a>
                  <span className="text-gray-300">|</span>
                  <a href="#" className="hover:underline">Accessibility</a>
                  <span className="text-gray-300">|</span>
                  <a href="#" className="hover:underline">Help & Support</a>
                </div>
              </div>
            </footer>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
