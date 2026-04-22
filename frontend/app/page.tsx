"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { Activity, AlertCircle, CheckCircle2, Clock } from "lucide-react";

const API_BASE = "http://localhost:8000/api";

export default function CommandCenter() {
  const [health, setHealth] = useState([]);
  const [queue, setQueue] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const hRes = await axios.get(`${API_BASE}/health/status`);
        const qRes = await axios.get(`${API_BASE}/queue/pending`);
        setHealth(hRes.data.data);
        setQueue(qRes.data.data);
      } catch (err) {
        console.error("Failed to fetch data", err);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Command Center</h1>
        <p className="text-slate-400">Global repository health and pending approvals.</p>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {health.map((repo, i) => (
          <div key={i} className="p-6 rounded-xl bg-slate-900 border border-slate-800">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-semibold">{repo.repo}</h3>
              <div className={`w-3 h-3 rounded-full ${
                repo.status === "Green" ? "bg-health-green" : 
                repo.status === "Yellow" ? "bg-health-yellow" : "bg-health-red"
              }`} />
            </div>
            <div className="text-4xl font-bold mb-2">{repo.health_score}%</div>
            <div className="text-sm text-slate-400">Health Score</div>
            <div className="mt-4 text-xs text-slate-500">
              {repo.total_conflicts} Active Overlaps
            </div>
          </div>
        ))}
      </section>

      <section className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden">
        <div className="p-6 border-b border-slate-800 flex justify-between items-center">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <Clock size={20} /> Pending HITL Queue
          </h2>
          <span className="px-3 py-1 rounded-full bg-brand-primary/20 text-brand-primary text-xs font-medium">
            {queue.length} Pending
          </span>
        </div>
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-800/50 text-slate-400">
            <tr>
              <th className="p-4 font-medium">ID</th>
              <th className="p-4 font-medium">Repository</th>
              <th className="p-4 font-medium">Priority</th>
              <th className="p-4 font-medium">Created</th>
              <th className="p-4 font-medium text-right">Action</th>
            </tr>
          </thead>
          <tbody>
            {queue.map((item) => (
              <tr key={item.id} className="border-t border-slate-800 hover:bg-slate-800/30 transition-colors">
                <td className="p-4 font-mono text-slate-400">{item.id.slice(0,8)}...</td>
                <td className="p-4">{item.repo}</td>
                <td className="p-4">
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    item.priority === "high" ? "bg-red-500/20 text-red-400" : "bg-slate-700 text-slate-300"
                  }`}>
                    {item.priority}
                  </span>
                </td>
                <td className="p-4 text-slate-500">{new Date(item.created_at).toLocaleString()}</td>
                <td className="p-4 text-right">
                  <button className="px-3 py-1 bg-brand-primary text-white rounded text-xs hover:bg-blue-600 transition-colors">
                    Review
                  </button>
                </td>
              </tr>
            ))}
            {queue.length === 0 && (
              <tr>
                <td colSpan="5" className="p-12 text-center text-slate-500">
                  <div className="flex flex-col items-center gap-2">
                    <CheckCircle2 size={40} className="text-health-green opacity-50" />
                    <p>All conflicts resolved. The pipeline is clear!</p>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </div>
  );
}
