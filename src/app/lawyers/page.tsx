'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Search, SlidersHorizontal } from 'lucide-react';
import LawyerCard from '../components/LawyerCard'; // Import the new component

// --- FAKE MOCK DATA ---
// We will replace this with a database call later
const mockLawyers = [
    {
        id: '1',
        name: 'Adv. Priya Sharma',
        specialization: 'Family Law',
        bio: 'Expert in divorce, child custody, and alimony cases with over 10 years of experience. Compassionate and dedicated to my clients.',
        ratePerSlot: 2000,
        isVerified: true,
        rating: 4.9,
        reviewCount: 120,
        imageUrl: 'https://i.pravatar.cc/150?img=1' // Placeholder image
    },
    {
        id: '2',
        name: 'Adv. Rohan Gupta',
        specialization: 'Real Estate Law',
        bio: 'Specializing in property disputes, lease agreements, and land registration. I ensure your property transactions are secure and legal.',
        ratePerSlot: 1500,
        isVerified: true,
        rating: 4.8,
        reviewCount: 85,
        imageUrl: 'https://i.pravatar.cc/150?img=2' // Placeholder image
    },
    {
        id: '3',
        name: 'Adv. Anjali Singh',
        specialization: 'Corporate Law',
        bio: 'Helping startups and businesses with contracts, compliance, and intellectual property. Your business is my priority.',
        ratePerSlot: 3000,
        isVerified: true,
        rating: 4.9,
        reviewCount: 92,
        imageUrl: 'https://i.pravatar.cc/150?img=3' // Placeholder image
    },
    {
        id: '4',
        name: 'Adv. Vikram Reddy',
        specialization: 'Criminal Law',
        bio: 'Dedicated defense attorney providing robust legal representation for a wide range of criminal charges. I fight for your rights.',
        ratePerSlot: 2500,
        isVerified: false, // Example of unverified
        rating: 4.7,
        reviewCount: 74,
        imageUrl: 'https://i.pravatar.cc/150?img=4' // Placeholder image
    },
];
// --- END OF FAKE DATA ---

export default function LawyersMarketplacePage() {
    // In the future, we will fetch lawyers here
    // const [lawyers, setLawyers] = useState([]);
    // useEffect(() => {
    //   fetch('/api/lawyers').then(res => res.json()).then(data => setLawyers(data));
    // }, []);

    const lawyers = mockLawyers; // Use mock data for now

    return (
        <main className="flex flex-col items-center min-h-screen p-4 bg-slate-900 text-white">
            <div className="w-full max-w-6xl mx-auto px-4 py-12">
                <Link href="/" className="inline-flex items-center mb-6 text-sky-400 hover:underline">
                    <ArrowLeft className="w-5 h-5 mr-2" />
                    Back to Home
                </Link>

                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-white">Find Your Lawyer</h1>
                    <p className="text-lg text-slate-300 mt-2">
                        Get a second opinion from a verified legal professional.
                    </p>
                </div>

                {/* --- Search and Filter Bar --- */}
                <div className="mb-8 p-4 bg-slate-800/50 rounded-xl border border-slate-700/50 flex flex-col md:flex-row gap-4">
                    <div className="relative flex-grow">
                        <input
                            type="text"
                            placeholder="Search by name or specialization (e.g., 'Family Law')"
                            className="w-full bg-slate-900 border border-slate-700 rounded-lg py-3 pl-10 pr-4 text-white focus:outline-none focus:ring-2 focus:ring-sky-500"
                        />
                        <Search className="w-5 h-5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                    </div>
                    <button className="flex-shrink-0 flex items-center justify-center gap-2 bg-slate-700 text-white font-semibold py-3 px-6 rounded-lg hover:bg-slate-600 transition-colors">
                        <SlidersHorizontal className="w-5 h-5" />
                        <span>Filters</span>
                    </button>
                </div>

                {/* --- Lawyers Grid --- */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {lawyers.map((lawyer) => (
                        <LawyerCard key={lawyer.id} lawyer={lawyer} />
                    ))}
                </div>
            </div>
        </main>
    );
}