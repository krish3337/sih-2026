import React, { useState, useRef, useEffect } from 'react';
import { HelpCircle, Activity, BookOpen, MessageSquare, Mail, Type, Contrast, Check } from 'lucide-react';

export default function Header() {
  const [activeDropdown, setActiveDropdown] = useState(null); // 'help', 'accessibility', or null
  const headerRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (headerRef.current && !headerRef.current.contains(event.target)) {
        setActiveDropdown(null);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const toggleDropdown = (dropdown) => {
    setActiveDropdown(activeDropdown === dropdown ? null : dropdown);
  };

  return (
    <div className="flex flex-col relative z-50" ref={headerRef}>
      <header className="bg-[#0b1b3d] text-white shadow-md">
        <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20 items-center">
            
            {/* Logo and Titles */}
            <div className="flex items-center space-x-4">
              <div className="h-12 w-16 bg-white/10 rounded flex flex-col items-center justify-center border border-white/20 shrink-0">
                <div className="relative flex items-center justify-center flex-1 w-full pt-1">
                  <span className="text-[22px] font-black text-white tracking-wider leading-none z-10">IS</span>
                  <Check className="absolute text-green-400 w-9 h-9 opacity-50 z-20 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" strokeWidth={3} />
                </div>
                <span className="text-[6px] font-bold tracking-widest text-white uppercase pb-1 z-10">StandSure</span>
              </div>
              <div className="flex flex-col justify-center">
                <h1 className="text-xl font-bold tracking-tight text-white leading-tight">StandSure</h1>
                <div className="flex items-center text-xs text-gray-300 mt-0.5 space-x-2">
                  <span>Government of India</span>
                  <span className="text-gray-500">|</span>
                  <span>AI Division</span>
                </div>
              </div>
              
              <div className="hidden md:block h-10 w-px bg-white/20 mx-4"></div>
              
              <div className="hidden lg:flex flex-col justify-center text-xs text-gray-300 leading-tight">
                <span>Digital Platform for</span>
                <span>Indian Standards Intelligence</span>
              </div>
            </div>

            {/* Right Actions */}
            <div className="flex items-center space-x-2 sm:space-x-6 text-sm font-medium relative">
              
              {/* Help Dropdown */}
              <div className="relative">
                <button 
                  onClick={() => toggleDropdown('help')}
                  className={`flex items-center px-2 py-1 rounded transition-colors ${activeDropdown === 'help' ? 'bg-white/10 text-white' : 'hover:text-gray-300'}`}
                >
                  <HelpCircle className="w-4 h-4 mr-1.5" />
                  <span className="hidden sm:inline">Help</span>
                </button>
                
                {activeDropdown === 'help' && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 text-gray-700 z-50">
                    <a href="#" className="flex items-center px-4 py-2 text-sm hover:bg-gray-100"><BookOpen className="w-4 h-4 mr-2 text-gray-400" /> User Guide</a>
                    <a href="#" className="flex items-center px-4 py-2 text-sm hover:bg-gray-100"><MessageSquare className="w-4 h-4 mr-2 text-gray-400" /> FAQs</a>
                    <div className="border-t border-gray-100 my-1"></div>
                    <a href="#" className="flex items-center px-4 py-2 text-sm hover:bg-gray-100"><Mail className="w-4 h-4 mr-2 text-gray-400" /> Contact Support</a>
                  </div>
                )}
              </div>

              {/* Accessibility Dropdown */}
              <div className="relative">
                <button 
                  onClick={() => toggleDropdown('accessibility')}
                  className={`flex items-center px-2 py-1 rounded transition-colors ${activeDropdown === 'accessibility' ? 'bg-white/10 text-white' : 'hover:text-gray-300'}`}
                >
                  <Activity className="w-4 h-4 mr-1.5" />
                  <span className="hidden sm:inline">Accessibility</span>
                </button>
                
                {activeDropdown === 'accessibility' && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg border border-gray-200 py-2 px-3 text-gray-700 z-50">
                    <div className="mb-3">
                      <p className="text-xs font-semibold text-gray-500 mb-2 uppercase flex items-center"><Type className="w-3 h-3 mr-1" /> Text Size</p>
                      <div className="flex justify-between space-x-2">
                        <button className="flex-1 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded py-1 text-sm font-medium">A-</button>
                        <button className="flex-1 bg-[#1a365d] text-white border border-[#1a365d] rounded py-1 text-sm font-medium">A</button>
                        <button className="flex-1 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded py-1 text-sm font-medium">A+</button>
                      </div>
                    </div>
                    <div className="border-t border-gray-100 my-2"></div>
                    <div>
                      <p className="text-xs font-semibold text-gray-500 mb-2 uppercase flex items-center"><Contrast className="w-3 h-3 mr-1" /> Contrast</p>
                      <label className="flex items-center cursor-pointer text-sm">
                        <input type="checkbox" className="mr-2 rounded text-[#1a365d] focus:ring-[#1a365d]" />
                        High Contrast Mode
                      </label>
                    </div>
                  </div>
                )}
              </div>

            </div>

          </div>
        </div>
      </header>
      
      {/* Tricolor Strip */}
      <div className="h-1.5 w-full flex">
        <div className="h-full bg-[#FF9933] w-1/3"></div>
        <div className="h-full bg-white w-1/3"></div>
        <div className="h-full bg-[#138808] w-1/3"></div>
      </div>
    </div>
  );
}
