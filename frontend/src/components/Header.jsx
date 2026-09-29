import React, { useState, useRef, useEffect } from 'react';
import { HelpCircle, Activity, BookOpen, MessageSquare, Mail, Type, Contrast, Check } from 'lucide-react';
import logoImg from './logo.jpeg';

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
      <header className="bg-white text-[#1a365d] shadow-sm border-b border-gray-200">
        <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20 items-center">
            
            {/* Logo and Titles */}
            <div className="flex items-center space-x-4">
              <div className="h-12 flex items-center justify-center shrink-0">
                <img src={logoImg} alt="StandSure Logo" className="h-10 w-auto object-contain mix-blend-multiply" />
              </div>
              <div className="flex flex-col justify-center">
                <h1 className="text-xl font-bold tracking-tight text-[#1a365d] leading-tight">StandSure</h1>
                <div className="flex items-center text-xs text-gray-500 mt-0.5 space-x-2">
                  <span>Government of India</span>
                  <span className="text-gray-400">|</span>
                  <span>AI Division</span>
                </div>
              </div>
              
              <div className="hidden md:block h-10 w-px bg-gray-200 mx-4"></div>
              
              <div className="hidden lg:flex flex-col justify-center text-xs text-gray-500 leading-tight">
                <span>Digital Platform for</span>
                <span>Indian Standards Intelligence</span>
              </div>
            </div>

            {/* Right Actions removed as requested */}
            
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
