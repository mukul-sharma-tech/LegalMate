import { auth } from '@clerk/nextjs/server';
import { NextRequest } from 'next/server';
import connectDB from '@/lib/db';
import Lawyer from '@/lib/models/Lawyer';
import User from '@/lib/models/User';
import { handleApiError, createSuccessResponse, createErrorResponse } from '@/lib/utils/errorHandler';

// GET all lawyers with filters
export async function GET(req: NextRequest) {
  try {
    await connectDB();

    const { searchParams } = new URL(req.url);
    const specialization = searchParams.get('specialization');
    const language = searchParams.get('language');
    const minRating = searchParams.get('minRating');
    const maxFee = searchParams.get('maxFee');
    const search = searchParams.get('search');
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '12');

    // Build query
    const query: any = { isActive: true };

    if (specialization) {
      query.specializations = { $in: [specialization] };
    }

    if (language) {
      query.languagesSpoken = { $in: [language] };
    }

    if (minRating) {
      query.averageRating = { $gte: parseFloat(minRating) };
    }

    if (maxFee) {
      query['fees.perHour'] = { $lte: parseFloat(maxFee) };
    }

    // Get lawyers with populated user data
    const lawyers = await Lawyer.find(query)
      .populate('userId', 'firstName lastName email profileImage')
      .sort({ averageRating: -1, totalReviews: -1 })
      .skip((page - 1) * limit)
      .limit(limit)
      .lean();

    // Search by name if search param exists
    let filteredLawyers = lawyers;
    if (search) {
      filteredLawyers = lawyers.filter((lawyer: any) => {
        const fullName = `${lawyer.userId.firstName} ${lawyer.userId.lastName}`.toLowerCase();
        return fullName.includes(search.toLowerCase());
      });
    }

    const total = await Lawyer.countDocuments(query);

    return createSuccessResponse({
      lawyers: filteredLawyers,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    return handleApiError(error);
  }
}

// POST - Create lawyer profile (called during onboarding)
export async function POST(req: NextRequest) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return createErrorResponse('Unauthorized', 401);
    }

    await connectDB();

    const body = await req.json();

    // Check if lawyer profile already exists
    const existingLawyer = await Lawyer.findOne({ clerkId: userId });
    
    if (existingLawyer) {
      return createErrorResponse('Lawyer profile already exists', 400);
    }

    // Get user
    const user = await User.findOne({ clerkId: userId });
    
    if (!user) {
      return createErrorResponse('User not found', 404);
    }

    if (user.role !== 'lawyer') {
      return createErrorResponse('User is not a lawyer', 403);
    }

    // Create lawyer profile
    const lawyer = await Lawyer.create({
      userId: user._id,
      clerkId: userId,
      ...body
    });

    return createSuccessResponse(lawyer, 'Lawyer profile created', 201);
  } catch (error) {
    return handleApiError(error);
  }
}