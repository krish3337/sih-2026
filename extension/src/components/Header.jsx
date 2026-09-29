import { Shield, Globe } from 'lucide-react';

export default function Header({ language, setLanguage }) {
  return (
    <div className="flex flex-col relative">
      <header className="flex items-center justify-between px-4 py-3 bg-white text-[#1a365d] border-b border-gray-200 shadow-sm">
        <div className="flex items-center space-x-2">
          <Shield className="w-6 h-6 text-[#1a365d]" />
          <div>
            <h1 className="text-sm font-bold leading-tight tracking-tight">StandSure AI</h1>
            <p className="text-[10px] text-gray-500 font-medium">Govt. Standards Assistant</p>
          </div>
        </div>
        <div className="flex items-center space-x-1 bg-gray-50 rounded px-2 py-1 text-xs border border-gray-200">
          <Globe className="w-3 h-3 text-gray-500" />
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-transparent text-[#1a365d] outline-none cursor-pointer font-medium"
          >
            <option value="English">English</option>
            <option value="Hindi">Hindi</option>
            <option value="Tamil">Tamil</option>
            <option value="Telugu">Telugu</option>
          </select>
        </div>
      </header>
      
      {/* Tricolor Strip to perfectly match frontend */}
      <div className="h-1 w-full flex">
        <div className="h-full bg-[#FF9933] w-1/3"></div>
        <div className="h-full bg-white w-1/3"></div>
        <div className="h-full bg-[#138808] w-1/3"></div>
      </div>
    </div>
  );
}
