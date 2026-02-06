import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function NotFound() {
    return (
        <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6 selection:bg-white selection:text-black">
            <h1 className="text-9xl font-light mb-4">404</h1>
            <h2 className="text-2xl font-light mb-8">Page Not Found</h2>
            <p className="text-gray-500 font-light mb-12 max-w-md text-center">
                The page you are looking for has been moved or does not exist.
            </p>
            <Link href="/">
                <Button className="bg-white text-black hover:bg-gray-200 rounded-none px-8 h-12">
                    Return Home
                </Button>
            </Link>
        </div>
    )
}
