import { Loader2 } from 'lucide-react';

export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center flex-1 p-5 h-full space-y-4">
      <div className="bg-white p-4 rounded-full shadow-sm mb-2">
        <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
      </div>
      <h2 className="text-xl font-semibold text-slate-800">Analyzing Specification</h2>
      <p className="text-sm text-slate-500 text-center max-w-xs">
        Searching applicable Indian Standards...
      </p>
    </div>
  );
}
