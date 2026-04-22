"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import { AlertTriangle, CheckCircle, RotateCcw, PlayCircle } from "lucide-react";

const API_BASE = "http://localhost:8000/api";

export default function SafetySuite() {
  const [rules, setRules] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get(`${API_BASE}/safety/rules`).then(res => setRules(res.data.rules));
  }, []);

  const toggleRule = async (name, value) => {
    setLoading(true);
    await axios.post(`${API_BASE}/safety/rules/update?rule_name=${name}&value=${value}`);
    setRules(prev => ({ ...prev, [name]: value }));
    setLoading(false);
  };

  const triggerPanic = async () => {
    if (!confirm("SURE? This will revert the last merge on the production branch!")) return;
    try {
      await axios.post(`${API_BASE}/safety/revert?target_branch=main`);
      alert("Panic Revert successful!");
    } catch (err) {
      alert("Panic Revert failed.");
    }
  };

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Safety & Automation</h1>
        <p className="text-slate-400">Critical controls to prevent production outages.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <section className="p-6 rounded-xl bg-slate-900 border border-slate-800">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <RotateCcw size={20} className="text-red-400" /> The Panic Button
          </h2>
          <div className="p-8 border-2 border-dashed border-red-900/50 rounded-xl bg-red-950/10 text-center">
            <p className="text-slate-400 mb-6 text-sm">
              Instantly reverts the most recent AI-executed merge on the main branch and restores the previous stable state.
            </p>
            <button 
              onClick={triggerPanic}
              className="px-8 py-4 bg-red-600 text-white rounded-full font-bold hover:bg-red-700 transition-all transform hover:scale-105 shadow-lg shadow-red-600/20"
            >
              TRIGGER EMERGENCY REVERT
            </button>
          </div>
        </section>

        <section className="p-6 rounded-xl bg-slate-900 border border-slate-800">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <ShieldAlert size={20} className="text-brand-primary" /> Auto-Merge Rules
          </h2>
          <div className="space-y-4">
            {Object.entries(rules).map(([name, value]) => (
              <div key={name} className="flex justify-between items-center p-3 rounded-lg bg-slate-800/50">
                <span className="text-sm text-slate-300 capitalize">{name.replace(/_/g, ' ')}</span>
                <button 
                  onClick={() => toggleRule(name, !value)}
                  className={`w-12 h-6 rounded-full transition-colors relative ${value ? 'bg-brand-primary' : 'bg-slate-600'}`}
                >
                  <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${value ? 'right-1' : 'left-1'}`} />
                </button>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="p-6 rounded-xl bg-slate-900 border border-slate-800">
        <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
          <PlayCircle size={20} className="text-green-400" /> Dry-Run Sandbox
        </h2>
        <div className="flex gap-4">
          <input className="flex-1 p-3 rounded-lg bg-slate-800 border border-slate-700 outline-none focus:border-brand-primary" placeholder="Source Branch (e.g. feature/login)" id="src" />
          <input className="flex-1 p-3 rounded-lg bg-slate-800 border border-slate-700 outline-none focus:border-brand-primary" placeholder="Target Branch (e.g. main)" id="tgt" />
          <button className="px-6 py-3 bg-brand-primary text-white rounded-lg font-medium hover:bg-blue-600 transition-colors">
            Run Test Merge
          </button>
        </div>
        <div className="mt-6 p-4 rounded-lg bg-black/50 font-mono text-xs text-slate-400 border border-slate-800 h-40 overflow-y-auto">
          {`// Sandbox output will appear here...`}
        </div>
      </section>
    </div>
  );
}
