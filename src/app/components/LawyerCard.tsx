'use client';

import React from 'react';
import Link from 'next/link';
import { ShieldCheck, Scale, Star } from 'lucide-react';
import Image from "next/image";
// This is the (fake) data structure we'll use for now
export interface Lawyer {
    id: string;
    name: string;
    specialization: string;
    bio: string;
    ratePerSlot: number;
    isVerified: boolean;
    rating: number; // Example property
    reviewCount: number; // Example property
    imageUrl: string; // Example property
}

interface LawyerCardProps {
    lawyer: Lawyer;
}

export default function LawyerCard({ lawyer }: LawyerCardProps) {
    return (
        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50 shadow-lg hover:border-sky-500/50 hover:bg-slate-800 transition-all duration-300 flex flex-col">

            <div className="flex items-start gap-4 mb-4">

                <Image
                    src={lawyer.imageUrl}
                    alt={lawyer.name}
                    width={80} // 20 * 4 = 80px (Tailwind's w-20)
                    height={80} // 20 * 4 = 80px (Tailwind's h-20)
                    className="rounded-full border-2 border-sky-500 object-cover"
                />
                <div className="flex-grow">
                    <h3 className="text-2xl font-semibold text-white mb-1">{lawyer.name}</h3>
                    {lawyer.isVerified && (
                        <div className="flex items-center gap-1.5 text-xs text-green-400 mb-2">
                            <ShieldCheck className="w-4 h-4" />
                            Verified Professional
                        </div>
                    )}
                    <div className="flex items-center gap-1.5 text-sm text-sky-300">
                        <Scale className="w-4 h-4" />
                        {lawyer.specialization}
                    </div>
                </div>
            </div>

            <p className="text-slate-400 flex-grow mb-4 text-sm leading-relaxed">
                {lawyer.bio.substring(0, 100)}...
            </p>

            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-1 text-amber-400">
                    <Star className="w-5 h-5 fill-amber-400" />
                    <span className="font-bold text-white">{lawyer.rating.toFixed(1)}</span>
                    <span className="text-slate-400 text-sm">({lawyer.reviewCount} reviews)</span>
                </div>
                <div className="text-right">
                    <span className="text-2xl font-bold text-white">₹{lawyer.ratePerSlot}</span>
                    <span className="text-slate-400 text-sm">/ 30 min</span>
                </div>
            </div>

            <Link
                href={`/lawyers/${lawyer.id}`}
                className="w-full mt-auto bg-sky-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-sky-500 transition-colors block text-center"
            >
                View Profile & Book
            </Link>
        </div>
    );
}