import StandardCard from './StandardCard';

// Using a configurable URL as requested
const WEB_APP_URL = "http://localhost:5173";

export default function Results({ results, onReset }) {
  if (!results || !results.standards) return null;

  return (
    <div className="flex flex-col flex-1 p-5 overflow-y-auto bg-slate-50">
      <div className="mb-4 flex-shrink-0">
        <h2 className="text-xl font-semibold text-slate-800">Analysis Results</h2>
        <p className="text-sm text-emerald-700 mt-1 font-medium bg-emerald-50 inline-block px-2 py-0.5 rounded border border-emerald-200">
          {results.standards.length} Applicable Standards Found
        </p>
      </div>

      <div className="flex-1 mb-4 pb-2">
        {results.standards.map((std, idx) => (
          <StandardCard key={idx} {...std} />
        ))}
      </div>

      <div className="mt-auto space-y-3 pt-2 flex-shrink-0">
        <a
          href={WEB_APP_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="w-full py-2.5 bg-blue-700 hover:bg-blue-800 text-white font-medium rounded shadow-sm transition-colors flex justify-center text-center"
        >
          Open Full Analysis
        </a>
        
        <button
          onClick={onReset}
          className="w-full py-2.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-medium rounded shadow-sm transition-colors"
        >
          New Analysis
        </button>
      </div>
    </div>
  );
}
