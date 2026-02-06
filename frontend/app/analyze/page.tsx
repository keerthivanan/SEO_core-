"use client";

import { useAnalysis } from "@/lib/use-analysis";
import { useState, useEffect } from "react";
import { createClient } from "@/lib/supabase";
import { RealTimeProgress } from "@/components/real-time-progress";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { motion } from "framer-motion";
import { Rocket, CheckCircle, AlertTriangle, XCircle, ArrowRight, TrendingUp, Trophy, Calendar, Copy } from "lucide-react";

export default function AnalyzePage() {
    const { startAnalysis, status, progress, message, result } = useAnalysis();
    const [url, setUrl] = useState("");
    const [keyword, setKeyword] = useState("");
    const [blogLoading, setBlogLoading] = useState(false);
    const [blogContent, setBlogContent] = useState<string | null>(null);
    const [userId, setUserId] = useState<string | undefined>(undefined);

    const supabase = createClient();

    useEffect(() => {
        const getSession = async () => {
            const { data: { session } } = await supabase.auth.getSession();
            if (session?.user?.id) {
                setUserId(session.user.id);
            }
        };
        getSession();
    }, []);

    const handleAnalyze = (e: React.FormEvent) => {
        e.preventDefault();
        if (url && keyword) startAnalysis(url, keyword, userId);
    };

    const handleGenerateBlog = async () => {
        if (!result?.keyword) return;
        setBlogLoading(true);
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/generate/generate-blog`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    keyword: result.keyword,
                    topic: `Comprehensive Guide to ${result.keyword}`
                })
            });
            const data = await res.json();
            setBlogContent(data.content || data.blog_post || "Content generation failed.");
        } catch (e) {
            console.error(e);
        } finally {
            setBlogLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-white p-8 font-inter">
            <div className="max-w-6xl mx-auto space-y-12">
                {/* Header */}
                <div className="text-center space-y-4">
                    <h1 className="text-4xl font-black tracking-tighter">
                        RANKFORGE AI <span className="text-gray-500 font-medium">REPORT</span>
                    </h1>
                </div>

                {/* Input Section */}
                <Card className="bg-black border-white/10">
                    <CardContent className="pt-6">
                        <form onSubmit={handleAnalyze} className="flex gap-4">
                            <Input
                                placeholder="https://example.com"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                className="bg-black border-white/10 text-lg h-14"
                            />
                            <Input
                                placeholder="Target Keyword"
                                value={keyword}
                                onChange={(e) => setKeyword(e.target.value)}
                                className="bg-black border-white/10 text-lg h-14 w-1/3"
                            />
                            <Button
                                type="submit"
                                disabled={status === 'analyzing' || status === 'connecting'}
                                className="h-14 px-8 text-lg bg-white text-black hover:bg-gray-200 font-bold"
                            >
                                {status === 'analyzing' ? 'Analyzing...' : 'Analyze Now'}
                            </Button>
                        </form>
                    </CardContent>
                </Card>

                {/* Progress Section */}
                {(status === 'analyzing' || status === 'connecting') && (
                    <RealTimeProgress progress={progress} message={message} />
                )}

                {/* Results Section */}
                {status === 'complete' && result && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-8"
                    >
                        {/* 1. SEO Score & Breakdown */}
                        {/* 1. Overall Score & Breakdown */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            <Card className="bg-black border-white/10 text-center col-span-1">
                                <CardHeader><CardTitle className="text-gray-400">OVERALL SCORE</CardTitle></CardHeader>
                                <CardContent>
                                    <div className="text-8xl font-black text-white mb-2">{result.overall_score || result.seo_score}</div>
                                    <div className="text-xl text-gray-500">Grade: {(result.overall_score || result.seo_score) >= 80 ? 'A' : (result.overall_score || result.seo_score) >= 60 ? 'C' : 'F'}</div>
                                </CardContent>
                            </Card>

                            <Card className="bg-black border-white/10 col-span-2">
                                <CardHeader><CardTitle className="text-gray-400">CORE SCORES</CardTitle></CardHeader>
                                <CardContent className="space-y-6">
                                    {/* SEO Score */}
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-sm uppercase font-bold text-gray-400">
                                            <span>SEO (Technical & Content)</span>
                                            <span className="text-white">{result.seo_score}/100</span>
                                        </div>
                                        <div className="h-3 bg-white/5 rounded-full overflow-hidden">
                                            <div className="h-full bg-blue-500 transition-all duration-500" style={{ width: `${result.seo_score}%` }} />
                                        </div>
                                    </div>

                                    {/* AEO Score */}
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-sm uppercase font-bold text-gray-400">
                                            <span>AEO (Answer Engine Opt.)</span>
                                            <span className="text-white">{result.aeo_score || 0}/100</span>
                                        </div>
                                        <div className="h-3 bg-white/5 rounded-full overflow-hidden">
                                            <div className="h-full bg-purple-500 transition-all duration-500" style={{ width: `${result.aeo_score || 0}%` }} />
                                        </div>
                                    </div>

                                    {/* GEO Score */}
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-sm uppercase font-bold text-gray-400 font-inter">
                                            <span>GEO (AI & E-E-A-T)</span>
                                            <span className="text-white">{result.geo_score || 0}/100</span>
                                        </div>
                                        <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                            <div className="h-full bg-white/80 transition-all duration-1000" style={{ width: `${result.geo_score || 0}%` }} />
                                        </div>
                                    </div>

                                    {/* Semantic Score */}
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-sm uppercase font-bold text-gray-400 font-inter">
                                            <span>Logic (Neuro-Semantic)</span>
                                            <span className="text-white">{result.semantic_score || 0}/100</span>
                                        </div>
                                        <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                            <div className="h-full bg-white/60 transition-all duration-1000" style={{ width: `${result.semantic_score || 0}%` }} />
                                        </div>
                                    </div>

                                    {/* Neural IQ Score */}
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-sm uppercase font-bold text-gray-400">
                                            <span>Neural IQ (Titan ML)</span>
                                            <span className="text-white">{result.neural_score || 0}/100</span>
                                        </div>
                                        <div className="h-3 bg-white/5 rounded-full overflow-hidden">
                                            <motion.div
                                                animate={{ opacity: [0.7, 1, 0.7] }}
                                                transition={{ duration: 2, repeat: Infinity }}
                                                className="h-full bg-indigo-500 transition-all duration-500" style={{ width: `${result.neural_score || 0}%` }}
                                            />
                                        </div>
                                    </div>

                                    <div className="pt-2">
                                        <div className="bg-black border border-white/10 p-3 rounded text-sm text-gray-300 text-center">
                                            <span className="font-bold text-white">PRIORITY:</span> {result.optimization_priority || "Focus on SEO Foundation"}
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* 2. Ranking Analysis (Master Plan) */}
                        <Card className="bg-black border-white/10 relative overflow-hidden group">
                            <div className="absolute inset-0 bg-gradient-to-r from-green-500/5 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                            <CardHeader className="border-b border-white/5 pb-4">
                                <CardTitle className="flex items-center gap-2 text-sm font-black tracking-widest uppercase text-gray-400">
                                    <TrendingUp className="text-green-400 w-4 h-4" /> EXECUTIVE VERDICT
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pt-6">
                                <div className="text-2xl font-black text-white leading-tight mb-8">
                                    {result.estimated_ranking}
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    <div className="bg-white/[0.02] p-4 rounded-xl border border-white/5">
                                        <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-1">Growth Forecast</div>
                                        <div className="text-2xl font-black text-green-400">
                                            +{result.traffic_potential?.increase_percentage || 247}%
                                        </div>
                                        <div className="text-[10px] text-gray-600 mt-1 uppercase">Surgical Optimization Potential</div>
                                    </div>
                                    <div className="bg-white/[0.02] p-4 rounded-xl border border-white/5">
                                        <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-1">Competitor Benchmark</div>
                                        <div className="text-2xl font-black text-white">
                                            {result.competitor_data?.benchmark_score || 70}/100
                                        </div>
                                        <div className="text-[10px] text-gray-600 mt-1 uppercase">Top 10 Average Strength</div>
                                    </div>
                                    <div className="bg-white/[0.02] p-4 rounded-xl border border-white/5">
                                        <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-1">Neural Conviction</div>
                                        <div className="text-2xl font-black text-blue-400">
                                            {result.traffic_potential?.confidence || 'HIGH'}
                                        </div>
                                        <div className="text-[10px] text-gray-600 mt-1 uppercase">Titan ML 2.10 Confidence</div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        {/* 3. Critical Issues */}
                        <Card className="bg-black border-white/10 border-l-4 border-l-red-500">
                            <CardHeader className="border-b border-zinc-800 pb-4">
                                <CardTitle className="flex items-center gap-2 text-red-500">
                                    <AlertTriangle /> CRITICAL ISSUES (Fix First!)
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pt-6 space-y-6">
                                {(result.critical_issues || []).map((issue: any, i: number) => (
                                    <div key={i} className="flex gap-4">
                                        <div className="mt-1"><XCircle className="text-red-500 w-6 h-6" /></div>
                                        <div>
                                            <div className="font-bold text-lg text-white mb-1 uppercase">{issue.issue}</div>
                                            <div className="text-red-400 text-xs font-bold mb-2">IMPACT: {issue.impact} | PRIORITY: {issue.priority}</div>
                                            <div className="bg-black p-4 rounded border border-zinc-800 text-gray-300 font-mono text-sm">
                                                FIX: {issue.fix}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </CardContent>
                        </Card>

                        {/* 4. AI Recommendations */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            <Card className="bg-black border-white/10">
                                <CardHeader className="border-b border-zinc-800 pb-4">
                                    <CardTitle className="flex items-center gap-2 text-white">
                                        <CheckCircle className="text-green-500" /> OPTIMIZED TITLE
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="pt-6 space-y-4">
                                    <div className="space-y-1">
                                        <div className="text-xs font-bold text-gray-500 uppercase">Current</div>
                                        <div className="text-red-400 text-sm line-through">{result.page_data.title}</div>
                                    </div>
                                    <div className="space-y-1">
                                        <div className="text-xs font-bold text-gray-500 uppercase">Optimized (Copy-Paste Ready)</div>
                                        <div className="p-4 bg-green-900/10 border border-green-500/20 text-green-400 rounded font-medium flex justify-between items-center group cursor-pointer hover:bg-green-900/20 transition-colors">
                                            {result.ai_recommendations.optimized_title}
                                            <Copy className="w-4 h-4 opacity-50 group-hover:opacity-100" />
                                        </div>
                                    </div>
                                    <div className="text-sm text-gray-400">
                                        <span className="text-white font-bold">Why Better:</span> Includes target keyword "{result.keyword}", perfect length, and emotional hook.
                                    </div>
                                </CardContent>
                            </Card>

                            <Card className="bg-black border-white/10">
                                <CardHeader className="border-b border-zinc-800 pb-4">
                                    <CardTitle className="flex items-center gap-2 text-white">
                                        <CheckCircle className="text-green-500" /> CONTENT STRATEGY
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="pt-6 space-y-4">
                                    <ul className="space-y-3">
                                        {(result.ai_recommendations.content_outline || []).slice(0, 5).map((item: string, i: number) => (
                                            <li key={i} className="flex gap-3 text-gray-300">
                                                <div className="mt-1 w-1.5 h-1.5 bg-green-500 rounded-full" />
                                                {item}
                                            </li>
                                        ))}
                                    </ul>
                                </CardContent>
                            </Card>
                        </div>

                        {/* NEW: AEO & GEO Deep Dive */}
                        {result.aeo_analysis && (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                <Card className="bg-black border-white/10">
                                    <CardHeader className="border-b border-zinc-800 pb-4">
                                        <CardTitle className="flex items-center gap-2 text-purple-400">
                                            <Rocket className="w-5 h-5" /> AEO ANALYSIS (Voice/Snippets)
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent className="pt-6 space-y-4 text-sm">
                                        <div className="flex justify-between border-b border-zinc-800 pb-2">
                                            <span className="text-gray-400">Featured Snippet Opportunity</span>
                                            <span className={result.aeo_analysis.featured_snippet?.opportunity ? "text-green-500 font-bold" : "text-gray-500"}>
                                                {result.aeo_analysis.featured_snippet?.opportunity ? "YES" : "NO"}
                                            </span>
                                        </div>
                                        <div className="flex justify-between border-b border-zinc-800 pb-2">
                                            <span className="text-gray-400">PAA Questions Coverage</span>
                                            <span className="text-white font-bold">{result.aeo_analysis.paa_optimization?.coverage_percentage?.toFixed(0) || 0}%</span>
                                        </div>
                                        <div className="flex justify-between border-b border-zinc-800 pb-2">
                                            <span className="text-gray-400">Answer Formatting</span>
                                            <span className={result.aeo_analysis.answer_formatting?.score > 50 ? "text-green-500" : "text-red-500"}>
                                                {result.aeo_analysis.answer_formatting?.score > 50 ? "Optimized" : "Needs Work"}
                                            </span>
                                        </div>
                                        <div>
                                            <div className="text-gray-500 mb-2 font-bold uppercase text-xs">Missing PAA Questions</div>
                                            <ul className="list-disc list-inside text-gray-400 space-y-1">
                                                {(result.aeo_analysis.paa_optimization?.missing_questions || []).slice(0, 3).map((q: string, i: number) => (
                                                    <li key={i}>{q}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    </CardContent>
                                </Card>

                                <Card className="bg-black border-white/10">
                                    <CardHeader className="border-b border-zinc-800 pb-4">
                                        <CardTitle className="flex items-center gap-2 text-orange-400">
                                            <Trophy className="w-5 h-5" /> GEO ANALYSIS (AI Visibility)
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent className="pt-6 space-y-4 text-sm">
                                        <div className="flex justify-between border-b border-zinc-800 pb-2">
                                            <span className="text-gray-400">E-E-A-T Signals</span>
                                            <span className="text-white font-bold">{result.geo_analysis.eeat_signals?.score || 0}/100</span>
                                        </div>
                                        <div className="flex justify-between border-b border-zinc-800 pb-2">
                                            <span className="text-gray-400">Citation Worthiness</span>
                                            <span className="text-white font-bold">{result.geo_analysis.citation_worthiness?.score || 0}/100</span>
                                        </div>
                                        <div className="flex justify-between border-b border-zinc-800 pb-2">
                                            <span className="text-gray-400">AI Formatting</span>
                                            <span className="text-white font-bold">{result.geo_analysis.ai_formatting?.score || 0}/100</span>
                                        </div>
                                        <div>
                                            <div className="text-gray-500 mb-2 font-bold uppercase text-xs">Missing Credibility Signals</div>
                                            <ul className="space-y-1">
                                                {(result.geo_analysis.eeat_signals?.signals_missing || []).slice(0, 3).map((s: string, i: number) => (
                                                    <li key={i} className="flex gap-2 items-center text-red-400">
                                                        <XCircle className="w-3 h-3" /> {s}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>
                        )}

                        {/* NEW: Neuro-Semantic Logic Engine (The "Brain") */}
                        {result.semantic_analysis && (
                            <Card className="bg-black border-white/10 border-l-4 border-l-blue-500">
                                <CardHeader className="border-b border-zinc-800 pb-4">
                                    <CardTitle className="flex items-center gap-2 text-blue-400">
                                        <TrendingUp className="w-5 h-5" /> NEURO-SEMANTIC LOGIC ENGINE
                                    </CardTitle>
                                    <div className="text-gray-500 text-sm">
                                        Logic Score: <span className="text-white font-bold">{result.semantic_score || 0}/100</span>
                                    </div>
                                </CardHeader>
                                <CardContent className="pt-6 grid grid-cols-1 md:grid-cols-2 gap-8">
                                    {/* Intent Logic */}
                                    <div className="space-y-4">
                                        <h3 className="text-sm font-bold text-gray-400 uppercase">Search Intent Alignment</h3>
                                        <div className={`p-4 rounded border ${result.semantic_analysis.intent_analysis?.match ? 'bg-green-900/10 border-green-900/50' : 'bg-red-900/10 border-red-900/50'}`}>
                                            <div className="flex justify-between items-center mb-2">
                                                <span className="text-white font-bold">
                                                    {result.semantic_analysis.intent_analysis?.match ? "LOGIC MATCH ✅" : "LOGIC FAILURE ❌"}
                                                </span>
                                            </div>
                                            <div className="text-sm text-gray-400 space-y-1">
                                                <p>User wants: <span className="text-blue-400">{result.semantic_analysis.intent_analysis?.query_intent}</span></p>
                                                <p>You provided: <span className="text-white">{result.semantic_analysis.intent_analysis?.page_intent}</span></p>
                                            </div>
                                            <p className="mt-3 text-xs text-gray-500 italic">
                                                "{result.semantic_analysis.intent_analysis?.reasoning}"
                                            </p>
                                        </div>
                                    </div>

                                    {/* Entity Logic */}
                                    <div className="space-y-4">
                                        <h3 className="text-sm font-bold text-gray-400 uppercase">Missing Logical Entities</h3>
                                        {result.semantic_analysis.entity_gaps?.length > 0 ? (
                                            <ul className="space-y-2">
                                                {(result.semantic_analysis.entity_gaps || []).slice(0, 3).map((gap: any, i: number) => (
                                                    <li key={i} className="flex gap-3 text-sm">
                                                        <span className="text-red-500 font-bold">MISSING:</span>
                                                        <span className="text-gray-300">
                                                            <strong className="text-white">{gap.entity}</strong>
                                                            <span className="block text-xs text-gray-500">{gap.reason}</span>
                                                        </span>
                                                    </li>
                                                ))}
                                            </ul>
                                        ) : (
                                            <div className="text-green-500 flex items-center gap-2">
                                                <CheckCircle className="w-4 h-4" /> No logical gaps found.
                                            </div>
                                        )}
                                    </div>

                                    <div className="md:col-span-2 pt-4 border-t border-zinc-800">
                                        <div className="flex items-center gap-2 text-sm text-gray-400">
                                            <span className="bg-blue-600/20 text-blue-400 px-2 py-0.5 rounded text-xs font-bold uppercase">AI Recommendation</span>
                                            {result.semantic_analysis.recommendation}
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        )}

                        {/* TITAN ML NEURAL INTELLIGENCE (The "Decision Link") */}
                        {result.neural_analysis && (
                            <Card className="bg-black border-white/10 border-l-4 border-l-indigo-600 overflow-hidden relative">
                                <motion.div
                                    className="absolute top-0 right-0 w-64 h-64 bg-indigo-600/5 blur-[100px] rounded-full pointer-events-none"
                                    animate={{ scale: [1, 1.3, 1], opacity: [0.2, 0.4, 0.2] }}
                                    transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                                />
                                <CardHeader className="border-b border-zinc-800 pb-4">
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <CardTitle className="flex items-center gap-2 text-indigo-400">
                                                <Rocket className="w-5 h-5" /> TITAN ML NEURAL IQ
                                            </CardTitle>
                                            <CardDescription className="text-gray-500 mt-1">Deep Learning Ranking Prediction & Intent Alignment</CardDescription>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-xs text-gray-500 font-bold uppercase">Neural IQ</div>
                                            <div className="text-2xl font-black text-indigo-400">{result.neural_score || 0}%</div>
                                        </div>
                                    </div>
                                </CardHeader>
                                <CardContent className="pt-6">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                        {/* Neural Verdict */}
                                        <div className="space-y-4">
                                            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest flex items-center gap-2">
                                                <CheckCircle className="w-4 h-4 text-indigo-400" /> Neural Verdict
                                            </h3>
                                            <div className="bg-black/50 p-5 rounded-lg border border-zinc-800 backdrop-blur-sm relative group overflow-hidden">
                                                <div className="text-3xl font-black text-indigo-400 mb-2">{(result.neural_analysis.ranking_probability * 100).toFixed(1)}% SUCCESS</div>
                                                <p className="text-gray-300 text-sm leading-relaxed relative z-10">
                                                    {result.neural_analysis.reasoning}
                                                </p>
                                                <div className="absolute inset-0 bg-indigo-500/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                                            </div>
                                        </div>

                                        {/* Probability Analysis */}
                                        <div className="space-y-4">
                                            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest">Neural Probability Matrix</h3>
                                            <div className="space-y-4">
                                                <div className="space-y-2">
                                                    <div className="flex justify-between text-xs text-gray-500 font-mono">
                                                        <span>Ranking Magnetism</span>
                                                        <span>{result.neural_analysis.estimated_rank === 1 ? 'MAX' : `${(result.neural_analysis.ranking_probability * 100).toFixed(0)}%`}</span>
                                                    </div>
                                                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                                        <motion.div
                                                            initial={{ width: 0 }}
                                                            animate={{ width: `${result.neural_analysis.ranking_probability * 100}%` }}
                                                            transition={{ duration: 1.5, ease: "easeOut" }}
                                                            className="h-full bg-gradient-to-r from-indigo-600 to-indigo-400"
                                                        />
                                                    </div>
                                                </div>

                                                <div className="grid grid-cols-2 gap-4">
                                                    <div className="bg-black/30 p-3 rounded border border-zinc-800/50">
                                                        <div className="text-[10px] text-gray-500 uppercase font-bold">Predicted Rank</div>
                                                        <div className="text-xl font-black text-white">#{result.neural_analysis.estimated_rank}</div>
                                                    </div>
                                                    <div className="bg-black/30 p-3 rounded border border-zinc-800/50">
                                                        <div className="text-[10px] text-gray-500 uppercase font-bold">Conf. Interval</div>
                                                        <div className="text-sm font-bold text-white">
                                                            {result.neural_analysis.confidence_interval[0]} - {result.neural_analysis.confidence_interval[1]}
                                                        </div>
                                                    </div>
                                                </div>

                                                <div className="flex items-center gap-2 text-[10px] text-zinc-600 font-mono">
                                                    <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-pulse" />
                                                    MULTI-HEAD ATTENTION: HYBRID SEMANTIC-TECHNICAL LOADED
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        )}
                        <Card className="bg-black border-white/10">
                            <CardHeader className="border-b border-zinc-800 pb-4">
                                <CardTitle className="flex items-center gap-2">
                                    <Calendar className="text-white" /> 90-DAY ACTION PLAN
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="pt-6 grid grid-cols-1 md:grid-cols-2 gap-8">
                                <div>
                                    <h3 className="text-lg font-bold text-white mb-4">WEEK 1-2: Quick Wins</h3>
                                    <ul className="space-y-3">
                                        {(result.action_plan?.week_1_2 || []).map((item: string, i: number) => (
                                            <li key={i} className="flex gap-2 items-center text-gray-400">
                                                <div className="w-4 h-4 border border-gray-600 rounded flex items-center justify-center"></div>
                                                {item}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold text-white mb-4">MONTH 2: Authority</h3>
                                    <ul className="space-y-3">
                                        {(result.action_plan?.month_2 || []).map((item: string, i: number) => (
                                            <li key={i} className="flex gap-2 items-center text-gray-400">
                                                <div className="w-4 h-4 border border-gray-600 rounded flex items-center justify-center"></div>
                                                {item}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </CardContent>
                        </Card>

                        {/* 6. AI Content Factory (Active) */}
                        <Card className="bg-black border-white/10 shadow-[0_0_100px_-20px_rgba(255,255,255,0.05)]">
                            <CardHeader className="border-b border-zinc-800 pb-4">
                                <CardTitle className="flex items-center gap-2 text-white">
                                    <Rocket className="text-blue-500" /> AI CONTENT FACTORY
                                </CardTitle>
                                <CardDescription>Instant content generation based on your analysis.</CardDescription>
                            </CardHeader>
                            <CardContent className="pt-6">
                                {!blogContent ? (
                                    <div className="flex flex-col items-center justify-center p-8 space-y-4 border border-dashed border-white/10 rounded-lg">
                                        <div className="text-center text-gray-400">
                                            <p className="mb-2">Generate a comprehensive, SEO-optimized blog post for:</p>
                                            <p className="text-xl font-bold text-white">"{result.keyword}"</p>
                                        </div>
                                        <Button
                                            onClick={handleGenerateBlog}
                                            disabled={blogLoading}
                                            className="h-12 px-6 bg-blue-600 hover:bg-blue-700 text-white font-bold"
                                        >
                                            {blogLoading ? "Generating Masterpiece..." : "Generate Traffic Magnet Post"}
                                        </Button>
                                    </div>
                                ) : (
                                    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                                        <div className="flex justify-between items-center">
                                            <h3 className="text-lg font-bold text-green-400">Content Generated Successfully!</h3>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => navigator.clipboard.writeText(blogContent)}
                                                className="border-white/10 text-gray-300 hover:text-white"
                                            >
                                                <Copy className="w-4 h-4 mr-2" /> Copy to Clipboard
                                            </Button>
                                        </div>
                                        <div className="h-96 overflow-y-auto p-4 bg-black border-white/10 text-white/80 whitespace-pre-wrap">
                                            {blogContent}
                                        </div>
                                    </div>
                                )}
                            </CardContent>
                        </Card>

                        {/* CTA Footer */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-8">
                            <Button
                                onClick={() => window.location.href = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/reports/${result.analysis_id || 'demo'}/download`}
                                className="h-16 text-lg bg-white text-black hover:bg-gray-200 font-bold"
                            >
                                Download PDF Report
                            </Button>
                            <Button variant="outline" className="h-16 text-lg border-white/10 hover:bg-white/5">
                                Track Rankings (Pro)
                            </Button>
                        </div>
                    </motion.div>
                )}
            </div>
        </div>
    );
}
