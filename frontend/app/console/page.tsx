"use client";
import { useState } from "react";
import axios from "axios";
import { Send, Bot, User } from "lucide-react";

const API_BASE = "http://localhost:8000/api";

export default function AIConsole() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hello! I'm OpenClaw. Tell me which repositories to scan or which Jira tickets to summarize." }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      // In a real app, this would go to an LLM-powered route
      // For prototype, we simulate a response
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          role: "bot", 
          text: `I've received your command: "${input}". I'm analyzing the codebase now...` 
        }]);
        setIsLoading(false);
      }, 1000);
    } catch (err) {
      setMessages(prev => [...prev, { role: "bot", text: "Sorry, I encountered an error processing that request." }]);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <header className="mb-8">
        <h1 className="text-3xl font-bold">AI Communication Console</h1>
        <p className="text-slate-400">Direct natural language interface for OpenClaw agents.</p>
      </header>

      <div className="flex-1 overflow-y-auto space-y-4 mb-6 p-4 bg-slate-900/50 rounded-xl border border-slate-800">
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            {msg.role === "bot" && <div className="p-2 rounded-lg bg-brand-primary text-white"><Bot size={20} /></div>}
            <div className={`max-w-xl p-4 rounded-2xl ${
              msg.role === "user" ? "bg-brand-primary text-white rounded-tr-none" : "bg-slate-800 text-slate-200 rounded-tl-none"
            }`}>
              {msg.text}
            </div>
            {msg.role === "user" && <div className="p-2 rounded-lg bg-slate-700 text-white"><User size={20} /></div>}
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-4 justify-start">
            <div className="p-2 rounded-lg bg-brand-primary text-white animate-pulse"><Bot size={20} /></div>
            <div className="p-4 rounded-2xl bg-slate-800 text-slate-400 italic rounded-tl-none">
              OpenClaw is thinking...
            </div>
          </div>
        )}
      </div>

      <div className="relative">
        <input 
          className="w-full p-4 pr-16 rounded-xl bg-slate-900 border border-slate-800 focus:border-brand-primary outline-none transition-all text-white"
          placeholder="e.g. Compare feature/req-1 and feature/req-2 in Repo 2..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button 
          onClick={handleSend}
          className="absolute right-2 top-2 p-2 bg-brand-primary text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}
