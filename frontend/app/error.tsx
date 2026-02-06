"use client"

import { useEffect } from "react"
import { Button } from "@/components/ui/button"

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    useEffect(() => {
        console.error(error)
    }, [error])

    return (
        <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6">
            <h1 className="text-2xl font-light mb-4">Something went wrong</h1>
            <p className="text-gray-500 font-light mb-8 max-w-md text-center">
                We encountered an unexpected error. Our team has been notified.
            </p>
            <div className="flex gap-4">
                <Button
                    onClick={() => reset()}
                    className="bg-white text-black hover:bg-gray-200 rounded-none px-6"
                >
                    Try Again
                </Button>
                <Button
                    variant="outline"
                    onClick={() => window.location.href = '/'}
                    className="border-white/20 text-white hover:bg-white hover:text-black rounded-none px-6"
                >
                    Return Home
                </Button>
            </div>
        </div>
    )
}
