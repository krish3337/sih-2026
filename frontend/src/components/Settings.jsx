import React, { useState } from 'react';
import { Settings as SettingsIcon, Globe, Palette, User, Save } from 'lucide-react';

export default function Settings() {
  const [theme, setTheme] = useState('light');
  const [appLang, setAppLang] = useState('en');

  return (
    <div className="card h-full overflow-y-auto">
      <div className="flex items-center mb-6 border-b border-gray-200 pb-4">
        <SettingsIcon className="h-8 w-8 text-government-blue mr-3" />
        <h1 className="text-2xl font-bold text-government-blue">Account Settings</h1>
      </div>

      <div className="max-w-3xl space-y-8">
        
        {/* User Details */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 flex items-center mb-4">
            <User className="h-5 w-5 mr-2 text-gray-500" />
            User Details
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input type="text" className="input-field bg-gray-50 text-gray-500" value="Official Government User" readOnly />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <input type="email" className="input-field bg-gray-50 text-gray-500" value="official@govportal.in" readOnly />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Department/Role</label>
              <input type="text" className="input-field bg-gray-50 text-gray-500" value="Standards Analysis Division" readOnly />
            </div>
          </div>
        </section>

        {/* Global Preferences */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 flex items-center mb-4">
            <Globe className="h-5 w-5 mr-2 text-gray-500" />
            Global Preferences
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Interface Language</label>
              <select 
                value={appLang}
                onChange={(e) => setAppLang(e.target.value)}
                className="input-field"
              >
                <option value="en">English (Default)</option>
                <option value="hi">Hindi (हिन्दी)</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">Changes the language of the application interface.</p>
            </div>
          </div>
        </section>

        {/* Appearance */}
        <section>
          <h2 className="text-lg font-semibold text-gray-800 flex items-center mb-4">
            <Palette className="h-5 w-5 mr-2 text-gray-500" />
            Appearance
          </h2>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Colour Theme</label>
            <div className="flex space-x-4">
              <label className={`border rounded-lg p-4 flex flex-col items-center cursor-pointer hover:bg-gray-50 transition-colors ${theme === 'light' ? 'border-government-blue ring-1 ring-government-blue' : 'border-gray-200'}`}>
                <input 
                  type="radio" 
                  name="theme" 
                  value="light" 
                  checked={theme === 'light'}
                  onChange={(e) => setTheme(e.target.value)}
                  className="sr-only"
                />
                <div className="w-16 h-10 bg-white border border-gray-300 rounded mb-2 shadow-sm"></div>
                <span className="text-sm font-medium">Light Mode</span>
              </label>
              
              <label className={`border rounded-lg p-4 flex flex-col items-center cursor-pointer hover:bg-gray-50 transition-colors ${theme === 'dark' ? 'border-government-blue ring-1 ring-government-blue' : 'border-gray-200'}`}>
                <input 
                  type="radio" 
                  name="theme" 
                  value="dark" 
                  checked={theme === 'dark'}
                  onChange={(e) => setTheme(e.target.value)}
                  className="sr-only"
                />
                <div className="w-16 h-10 bg-gray-800 border border-gray-700 rounded mb-2 shadow-sm flex items-center justify-center">
                  <div className="w-8 h-2 bg-gray-600 rounded"></div>
                </div>
                <span className="text-sm font-medium">Black Screen</span>
              </label>
            </div>
          </div>
        </section>

        {/* Save Actions */}
        <div className="pt-6 border-t border-gray-200 flex justify-end">
          <button className="btn-primary flex items-center">
            <Save className="w-4 h-4 mr-2" />
            Save Changes
          </button>
        </div>

      </div>
    </div>
  );
}
