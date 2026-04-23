"use client";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Send, Bot, User, Sparkles, Zap, Shield, BarChart } from "lucide-react";

const API_BASE = "http://localhost:8000/api";

export default function ChatHub() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get(`${API_BASE}/chat/history`);
        setMessages(res.data.data);
      } catch (err) {
        console.error("Failed to load history", err);
      }
    };
    fetchHistory();
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (text = input) => {
    if (!text.trim()) return;
    
    const userMsg = { role: "user", text: text };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/chat/send`, { text: text });
      setMessages(prev => [...prev, { role: "bot", text: res.data.text }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: "bot", text: "I'm having trouble connecting to the brain. Please check the backend." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const quickCommands = [
    { label: "Health Scan", cmd: "Scan the health of the repos", icon: <BarChart size={14}/> },
    { label: "SIT Check", cmd: "Check for overlapping branches in SIT", icon: <Zap size={14}/> },
    { label: "Panic Revert", cmd: "Trigger panic revert", icon: <Shield size={14}/> },
    { label: "AI Summary", cmd: "Summarize the latest conflict", icon: <Sparkles size={14}/> },
  ];

  return (
    <div className="flex flex-col h-full max-w-5xl mx-auto">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <Bot className="text-brand-primary" size={32} />
            OpenClaw AI Hub
          </h1>
          <p className="text-slate-400">Your central command for AI-assisted development.</p>
        </div>
        <div className="px-4 py-2 rounded-full bg-green-500/10 text-green-400 text-xs font-medium border border-green-500/20 flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          System Online
        </div>
      </header>

      <div className="flex-1 overflow-y-auto space-y-6 mb-6 p-6 rounded-2xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center space-y-4 opacity-50">
            <Bot size={48} className="text-slate-600" />
            <p className="text-slate-400 max-w-xs">Welcome back. Send a command or use a shortcut to start managing your repositories.</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            {msg.role === "bot" && (
              <div className="p-2 rounded-lg bg-brand-primary text-white h-fit shadow-lg shadow-brand-primary/20">
                <Bot size={20} />
              </div>
            )}
            <div className={`max-w-2xl p-4 rounded-2xl ${
              msg.role === "user" ? "bg-brand-primary text-white rounded-tr-none shadow-md" : "bg-slate-800 text-slate-200 rounded-tl-none border border-slate-700"
            }`}>
              <p className="text-sm leading-relaxed">{msg.text}</p>
            </div>
            {msg.role === "user" && (
              <div className="p-2 rounded-lg bg-slate-700 text-white h-fit">
                <User size={20} />
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-4 justify-start">
            <div className="p-2 rounded-lg bg-brand-primary text-white animate-pulse"><Bot size={20} /></div>
            <div className="p-4 rounded-2xl bg-slate-800 text-slate-400 italic rounded-tl-none border border-slate-700">
              OpenClaw is analyzing...
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      <div className="space-y-4">
        <div className="flex flex-wrap gap-2">
          {quickCommands.map((cmd, i) => (
            <button 
              key={i} 
              onClick={() => handleSend(cmd.cmd)}
              className="px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-400 hover:text-white hover:bg-slate-700 transition-all flex items-center gap-2"
            >
              {cmd.icon} {cmd.label}
            </button>
          ))}
        </div>
        <div className="relative group">
          <input 
            className="w-full p-4 pr-16 rounded-2xl bg-slate-900 border border-slate-800 focus:border-brand-primary outline-none transition-all text-white shadow-2xl placeholder:text-slate-600"
            placeholder="Ask OpenClaw to perform a task..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button 
            onClick={() => handleSend()}
            className="absolute right-3 top-3 p-2 bg-brand-primary text-white rounded-xl hover:bg-blue-600 transition-all shadow-lg shadow-brand-primary/30"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
