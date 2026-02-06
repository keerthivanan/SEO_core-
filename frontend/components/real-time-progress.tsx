import { motion } from "framer-motion";

export function RealTimeProgress({ progress, message }: { progress: number, message: string }) {
    return (
        <div className="space-y-4 max-w-2xl mx-auto py-12">
            <div className="flex justify-between text-sm font-medium text-white/40">
                <span>{message}</span>
                <span>{progress}%</span>
            </div>
            <div className="h-4 bg-black rounded-full overflow-hidden border border-white/10">
                <motion.div
                    className="h-full bg-gradient-to-r from-indigo-500 to-cyan-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.5 }}
                />
            </div>
        </div>
    );
}
