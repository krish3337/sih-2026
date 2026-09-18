export default function SelectedText({ text, onAnalyze, onClear }) {
  return (
    <div className="flex flex-col flex-1 p-5 overflow-y-auto">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-slate-800">Selected Specification</h2>
        <p className="text-sm text-slate-500 mt-1">Review the text captured from the webpage.</p>
      </div>

      <div className="flex-1 bg-slate-100 border border-slate-200 rounded-md p-4 mb-5 overflow-y-auto max-h-[250px] shadow-inner text-sm text-slate-700 whitespace-pre-wrap">
        {text}
      </div>

      <div className="flex flex-col space-y-3 mt-auto">
        <button
          onClick={() => onAnalyze(text)}
          className="w-full py-2.5 bg-blue-700 hover:bg-blue-800 text-white font-medium rounded shadow-sm transition-colors"
        >
          Analyze Standards
        </button>

        <button
          onClick={onClear}
          className="w-full py-2.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-medium rounded shadow-sm transition-colors"
        >
          Clear
        </button>
      </div>
    </div>
  );
}
