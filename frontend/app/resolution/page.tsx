"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import { GitMerge, CheckCircle, AlertTriangle, FileText } from "lucide-react";

const API_BASE = "http://localhost:8000/api";

export default function ResolutionWorkspace() {
  const [diff, setDiff] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchDiff = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/resolution/diff`, {
        params: { branch_a: "feat1", branch_b: "feat2", proposal_branch: "proposal" }
      });
      setDiff(res.data);
    } catch (err) {
      alert("Failed to fetch diff");
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Resolution Workspace</h1>
          <p className="text-slate-400">Review AI proposals and refine logical merges.</p>
        </div>
        <button 
          onClick={fetchDiff}
          className="px-6 py-2 bg-brand-primary text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
        >
          {loading ? "Analyzing..." : "Generate Diff"}
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[70vh]">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2 text-sm font-medium text-slate-400">
            <FileText size={16} /> Branch A (Req 1)
          </div>
          <div className="flex-1 p-4 rounded-xl bg-slate-900 border border-slate-800 font-mono text-xs overflow-auto whitespace-pre">
            {diff?.branch_a_diff || "No diff available. Please generate diff."}
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2 text-sm font-medium text-slate-400">
            <FileText size={16} /> Branch B (Req 2)
          </div>
          <div className="flex-1 p-4 rounded-xl bg-slate-900 border border-slate-800 font-mono text-xs overflow-auto whitespace-pre">
            {diff?.branch_b_diff || "No diff available. Please generate diff."}
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2 text-sm font-medium text-brand-primary">
            <GitMerge size={16} /> OpenClaw Proposal
          </div>
          <div className="flex-1 p-4 rounded-xl bg-slate-900 border-2 border-brand-primary/30 font-mono text-xs overflow-auto whitespace-pre">
            {diff?.proposal_diff || "AI proposal will appear here."}
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-4">
        <button className="px-6 py-2 bg-slate-800 text-slate-300 rounded-lg hover:bg-slate-700 transition-colors">
          Request Changes
        </button>
        <button className="px-6 py-2 bg-health-green text-white rounded-lg font-bold hover:bg-green-600 transition-colors flex items-center gap-2">
          <CheckCircle size={18} /> Approve & Merge
        </button>
      </div>
    </div>
  );
}
