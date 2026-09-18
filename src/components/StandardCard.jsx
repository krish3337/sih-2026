import { ArrowRight } from 'lucide-react';

export default function StandardCard({ code, title, applicability, status, explanation }) {
  const isHigh = applicability === 'HIGH';
  const statusColor = isHigh ? 'text-emerald-700 bg-emerald-50 border-emerald-200' : 'text-slate-700 bg-slate-100 border-slate-200';

  return (
    <div className="bg-white border border-slate-200 rounded-md shadow-sm p-4 mb-3 hover:shadow-md transition-shadow">
      <h3 className="font-bold text-slate-900">{code}</h3>
      <p className="text-sm text-slate-700 mb-3">{title}</p>
      
      <div className="grid grid-cols-2 gap-2 text-xs mb-3">
        <div>
          <span className="text-slate-500 block mb-1">Applicability</span>
          <span className="font-semibold text-slate-800">{applicability}</span>
        </div>
        <div>
          <span className="text-slate-500 block mb-1">Status</span>
          <span className={`inline-block px-2 py-0.5 rounded text-[11px] font-medium border ${statusColor}`}>
            {status}
          </span>
        </div>
      </div>

      <p className="text-sm text-slate-600 mb-4 pb-4 border-b border-slate-100 leading-relaxed">
        {explanation}
      </p>

      <button className="text-blue-700 font-medium text-sm flex items-center hover:text-blue-800 transition-colors w-full justify-end group">
        View Details <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
      </button>
    </div>
  );
}
