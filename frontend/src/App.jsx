import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import HomeDashboard from './components/HomeDashboard';
import RecentAnalysis from './components/RecentAnalysis';
import MyDocuments from './components/MyDocuments';
import SplashScreen from './components/SplashScreen';
import { Shield, FileText, Languages, Lock, Users, Check } from 'lucide-react';
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
            
            {/* Footer */}
            <footer className="bg-white border-t border-gray-200 py-6 px-8 text-xs text-gray-500 flex flex-col md:flex-row justify-between items-start md:items-center shrink-0 space-y-6 md:space-y-0">
              
              {/* Logo & Hackathon Info */}
              <div className="flex items-center space-x-4">
                <div className="h-12 w-16 bg-gray-50 rounded flex flex-col items-center justify-center border border-gray-200 shrink-0">
                  <div className="relative flex items-center justify-center flex-1 w-full pt-1">
                    <span className="text-[22px] font-black text-[#0b1b3d] tracking-wider leading-none z-10">IS</span>
                    <Check className="absolute text-green-500 w-9 h-9 opacity-50 z-20 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" strokeWidth={3} />
                  </div>
                  <span className="text-[6px] font-bold tracking-widest text-[#0b1b3d] uppercase pb-1 z-10">StandSure</span>
                </div>
                <div className="flex flex-col">
                  <p className="font-semibold text-government-blue text-sm">Built for Smart India Hackathon 2026</p>
                  <p>Problem Statement: <span className="font-medium">SIH26108</span> by Ministry of Social Justice and Empowerment</p>
                </div>
              </div>
              
              {/* Disclaimer */}
              <div className="text-left md:text-center max-w-md">
                <p className="italic">Disclaimer: This platform is a prototype developed for hackathon demonstration purposes.</p>
              </div>
              
              {/* Copyright */}
              <div className="flex flex-col items-start md:items-end w-full md:w-auto">
                <p className="font-semibold text-government-blue">© 2026 Team PRACTICE MATCH</p>
              </div>
            </footer>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
