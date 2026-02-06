import { useState, useRef, useEffect, useCallback } from 'react';

type AnalysisResult = {
    analysis_id: string;
    url: string;
    keyword: string;
    seo_score: number;
    aeo_score: number;
    geo_score: number;
    semantic_score: number;
    neural_score: number; // New Titan ML Signal
    overall_score: number;
    optimization_priority: string;
    score_details: any;
    ai_recommendations: any;
    page_data: any;
    critical_issues: any[];
    action_plan: any;
    traffic_potential: any;
    estimated_ranking: string;
    aeo_analysis: any;
    geo_analysis: any;
    semantic_analysis: any;
    neural_analysis: any; // Detailed reasoning
};

type AnalysisStatus = 'idle' | 'connecting' | 'analyzing' | 'complete' | 'error';

export function useAnalysis() {
    const [status, setStatus] = useState<AnalysisStatus>('idle');
    const [progress, setProgress] = useState(0);
    const [message, setMessage] = useState('');
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const socketRef = useRef<WebSocket | null>(null);

    const startAnalysis = useCallback((url: string, keyword: string, userId?: string) => {
        setStatus('connecting');
        setProgress(0);
        setMessage('Connecting to RankForge AI...');
        setResult(null);

        // Close existing connection
        if (socketRef.current) {
            socketRef.current.close();
        }

        // Scale Optimized: Use environment variable for production deployment
        const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
        const ws = new WebSocket(`${wsUrl}/ws/analyze`);
        socketRef.current = ws;

        ws.onopen = () => {
            setStatus('analyzing');
            // Pass userId to the neural pipeline for multi-tenant isolation
            ws.send(JSON.stringify({
                url,
                target_keyword: keyword,
                user_id: userId || 'guest'
            }));
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);

                if (data.type === 'progress') {
                    setProgress(data.progress);
                    setMessage(data.message);
                } else if (data.type === 'complete') {
                    setResult(data.results);
                    setStatus('complete');
                    ws.close();
                } else if (data.type === 'error') {
                    setMessage(data.message);
                    setStatus('error');
                    ws.close();
                }
            } catch (e) {
                console.error('Parse error', e);
            }
        };

        ws.onerror = (e) => {
            console.error('WebSocket error', e);
            setMessage('Connection error. Is the backend running?');
            setStatus('error');
        };

        ws.onclose = () => {
            if (status !== 'complete' && status !== 'error') {
                // setMessage('Connection closed');
            }
        };

    }, [status]);

    return { startAnalysis, status, progress, message, result };
}
