import { useState, useEffect } from 'react';
import Header from './components/Header';
import Home from './components/Home';
import SelectedText from './components/SelectedText';
import Loading from './components/Loading';
import Results from './components/Results';
import EmptyState from './components/EmptyState';
import { analyzeSpecification } from './services/api';

export default function App() {
  const [view, setView] = useState('HOME');
  const [specificationText, setSpecificationText] = useState('');
  const [results, setResults] = useState(null);
  const [language, setLanguage] = useState('English');

  // Initialize from storage
  useEffect(() => {
    if (typeof chrome !== 'undefined' && chrome.storage) {
      chrome.storage.local.get(['selectedSpecificationText'], (result) => {
        if (result.selectedSpecificationText) {
          setSpecificationText(result.selectedSpecificationText);
          setView('SELECTED_TEXT');
          // Clear badge
          chrome.runtime.sendMessage({ action: "clearBadge" });
        }
      });
    }
  }, []);

  const handleAnalyzeSelected = () => {
    if (typeof chrome !== 'undefined' && chrome.tabs) {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
          chrome.tabs.sendMessage(tabs[0].id, { action: "getSelectedText" }, (response) => {
            if (chrome.runtime.lastError || !response || !response.text) {
              setView('ERROR');
            } else {
              setSpecificationText(response.text);
              setView('SELECTED_TEXT');
            }
          });
        }
      });
    } else {
      // Fallback for local development outside extension
      setView('ERROR');
    }
  };

  const handleAnalyze = async (payload) => {
    setView('LOADING');
    try {
      const data = await analyzeSpecification({
        ...payload,
        language
      });
      setResults(data);
      setView('RESULTS');
      // Clear storage after successful analysis
      if (typeof chrome !== 'undefined' && chrome.storage) {
        chrome.storage.local.remove('selectedSpecificationText');
      }
    } catch (error) {
      console.error(error);
      setView('ERROR');
    }
  };

  const handleClear = () => {
    setSpecificationText('');
    if (typeof chrome !== 'undefined' && chrome.storage) {
      chrome.storage.local.remove('selectedSpecificationText');
    }
    setView('HOME');
  };

  return (
    <div className="flex flex-col h-full bg-slate-50 font-sans text-slate-800">
      <Header language={language} setLanguage={setLanguage} />
      
      <main className="flex-1 flex flex-col min-h-0 relative">
        {view === 'HOME' && (
          <Home
            onAnalyze={handleAnalyze}
            onAnalyzeSelected={handleAnalyzeSelected}
          />
        )}

        {view === 'SELECTED_TEXT' && (
          <SelectedText
            text={specificationText}
            onAnalyze={(text) => handleAnalyze({ type: 'text', content: text })}
            onClear={handleClear}
          />
        )}

        {view === 'LOADING' && <Loading />}

        {view === 'RESULTS' && (
          <Results
            results={results}
            onReset={handleClear}
          />
        )}

        {view === 'ERROR' && (
          <EmptyState
            message="No specification selected"
            subMessage="Select relevant text from the tender webpage or enter the specification manually."
            buttonText="Enter Specification"
            onAction={() => setView('HOME')}
          />
        )}
      </main>
    </div>
  );
}
