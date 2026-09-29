import React, { useEffect, useState } from 'react';

export default function SplashScreen({ onComplete }) {
  const [phase, setPhase] = useState('initial');

  useEffect(() => {
    // Wait slightly for the user to read "StandSure" normally
    const t1 = setTimeout(() => {
      setPhase('animate');
    }, 300); 

    // After animation is fully enjoyed, fade out
    const t2 = setTimeout(() => {
      setPhase('fadeout');
      setTimeout(onComplete, 300);
    }, 1000); 

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [onComplete]);

  return (
    <div 
      className={`fixed inset-0 z-50 flex items-center justify-center bg-gray-50 transition-opacity duration-300 ease-in-out ${
        phase === 'fadeout' ? 'opacity-0' : 'opacity-100'
      }`}
    >
      <div className="w-full max-w-3xl px-6 md:px-12">
        <svg viewBox="0 0 800 300" className="w-full h-auto drop-shadow-2xl">
          <defs>
            <linearGradient id="logo-bg" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#0052cc" />
              <stop offset="100%" stopColor="#003d99" />
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="4" stdDeviation="4" floodOpacity="0.2" />
            </filter>
          </defs>

          {/* Outer Ring */}
          <ellipse cx="400" cy="150" rx="385" ry="135" fill="none" stroke="#003d99" strokeWidth="12" />
          
          {/* Inner Background */}
          <clipPath id="inner-clip">
            <ellipse cx="400" cy="150" rx="370" ry="120" />
          </clipPath>
          
          <g clipPath="url(#inner-clip)">
            <rect x="0" y="0" width="800" height="300" fill="url(#logo-bg)" />
            {/* Top White Wave */}
            <path d="M -50 130 C 250 70, 550 110, 850 150 L 850 -50 L -50 -50 Z" fill="#ffffff" />
            {/* Bottom White Wave */}
            <path d="M -50 235 C 250 245, 550 230, 850 240 L 850 350 L -50 350 Z" fill="#ffffff" />
          </g>

          {/* Text Group */}
          <g fontFamily="system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" fontWeight="900" fontSize="120" letterSpacing="-2">
            
            {/* Permanent Letters */}
            <g fill="#ffffff" filter="url(#shadow)">
              <text x="75" y="220">S</text>
              <text x="245" y="220">a</text>
              <text x="325" y="220">n</text>
              <text x="405" y="220">d</text>
              <text x="490" y="220">S</text>
              <text x="565" y="220">u</text>
              <text x="705" y="220">e</text>
            </g>

            {/* Letter 't' - Fades Out with style */}
            <text 
              x="170" y="220" fill="#ffffff" filter="url(#shadow)"
              className="transition-all duration-300 ease-in-out origin-[185px_160px]"
              style={{
                opacity: phase === 'animate' ? 0 : 1,
                transform: phase === 'animate' ? 'scale(1.3) translateY(-20px)' : 'scale(1) translateY(0px)'
              }}
            >
              t
            </text>

            {/* Letter 'r' - Fades Out with style */}
            <text 
              x="635" y="220" fill="#ffffff" filter="url(#shadow)"
              className="transition-all duration-300 ease-in-out origin-[680px_160px]"
              style={{
                opacity: phase === 'animate' ? 0 : 1,
                transform: phase === 'animate' ? 'scale(1.3) translateY(-20px)' : 'scale(1) translateY(0px)'
              }}
            >
              r
            </text>
          </g>

          {/* Orange Man (t) - Animates IN */}
          <g 
            className="transition-all duration-300 ease-out origin-[185px_160px]"
            style={{
              opacity: phase === 'animate' ? 1 : 0,
              transform: phase === 'animate' ? 'scale(1) translateY(0px)' : 'scale(0.5) translateY(30px)'
            }}
            filter="url(#shadow)"
          >
            {/* Exactly recreates the orange human figure from logo.jpeg */}
            <circle cx="185" cy="115" r="16" fill="#F26522" />
            <path d="M 150 145 L 220 145" fill="none" stroke="#F26522" strokeWidth="16" strokeLinecap="round" />
            <path d="M 185 145 L 185 185" fill="none" stroke="#F26522" strokeWidth="18" strokeLinecap="round" />
            <path d="M 185 185 Q 170 205 165 225" fill="none" stroke="#F26522" strokeWidth="16" strokeLinecap="round" />
            <path d="M 185 185 Q 200 205 205 225" fill="none" stroke="#F26522" strokeWidth="16" strokeLinecap="round" />
          </g>

          {/* Green Tick (r) - Animates IN */}
          <g 
            className="transition-all duration-300 ease-out origin-[680px_160px]"
            style={{
              opacity: phase === 'animate' ? 1 : 0,
              transform: phase === 'animate' ? 'scale(1) translateY(0px)' : 'scale(0.5) translateY(30px)'
            }}
            filter="url(#shadow)"
          >
            {/* Exactly recreates the green check mark from logo.jpeg overlapping the 'r' */}
            <path 
              d="M 635 175 L 655 200 Q 690 140 725 120" 
              fill="none" 
              stroke="#39B54A" 
              strokeWidth="24" 
              strokeLinecap="round" 
              strokeLinejoin="round" 
            />
          </g>
        </svg>
      </div>
    </div>
  );
}
