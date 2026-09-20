import { AlertCircle } from 'lucide-react';

export default function EmptyState({ message, subMessage, buttonText, onAction }) {
  return (
    <div className="flex flex-col items-center justify-center flex-1 p-5 h-full space-y-4 text-center">
      <div className="bg-slate-100 p-4 rounded-full text-slate-500 mb-2">
        <AlertCircle className="w-10 h-10" />
      </div>
      <h2 className="text-xl font-semibold text-slate-800">{message}</h2>
      <p className="text-sm text-slate-500 max-w-xs leading-relaxed">
        {subMessage}
      </p>
      {buttonText && onAction && (
        <button
          onClick={onAction}
          className="mt-6 px-6 py-2.5 bg-blue-700 hover:bg-blue-800 text-white font-medium rounded shadow-sm transition-colors"
        >
          {buttonText}
        </button>
      )}
    </div>
  );
}
