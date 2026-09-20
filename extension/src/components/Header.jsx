import { Shield, Globe } from 'lucide-react';

export default function Header({ language, setLanguage }) {
  return (
    <header className="flex items-center justify-between px-4 py-3 bg-slate-900 text-white shadow-md">
      <div className="flex items-center space-x-2">
        <Shield className="w-6 h-6 text-emerald-500" />
        <div>
          <h1 className="text-sm font-bold leading-tight">Indian Standards AI</h1>
          <p className="text-[10px] text-slate-300">Government Standards Assistant</p>
        </div>
      </div>
      <div className="flex items-center space-x-1 bg-slate-800 rounded px-2 py-1 text-xs">
        <Globe className="w-3 h-3 text-slate-400" />
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="bg-transparent text-white outline-none cursor-pointer"
        >
          <option value="English" className="bg-slate-800">English</option>
          <option value="Hindi" className="bg-slate-800">Hindi</option>
          <option value="Tamil" className="bg-slate-800">Tamil</option>
          <option value="Telugu" className="bg-slate-800">Telugu</option>
        </select>
      </div>
    </header>
  );
}
