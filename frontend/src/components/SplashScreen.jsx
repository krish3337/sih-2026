import React, { useEffect, useState } from 'react';

export default function SplashScreen({ onComplete }) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // 2.5 seconds total: 2s solid, 0.5s fade out
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(onComplete, 500); // Wait for fade out animation
    }, 2000);
    
    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div 
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-government-bg transition-opacity duration-500 ease-in-out ${
        isVisible ? 'opacity-100' : 'opacity-0'
      }`}
    >
      <div className="flex flex-col items-center">
        {/* Moving Circle Loader */}
        <div className="relative w-24 h-24 mb-8">
          <div className="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
          <div className="absolute inset-0 border-4 border-government-blue rounded-full border-t-transparent animate-spin"></div>
          <div className="absolute inset-0 border-4 border-green-500 rounded-full border-b-transparent animate-[spin_1.5s_linear_infinite_reverse]"></div>
        </div>
        
        {/* Flashing Name */}
        <h1 className="text-4xl font-bold text-government-blue animate-pulse text-center tracking-tight">
          StandSure
        </h1>
        <p className="text-gray-500 mt-2 text-sm tracking-widest uppercase">Initializing System...</p>
      </div>
    </div>
  );
}
