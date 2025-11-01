import { auth } from '@clerk/nextjs/server';
import { NextRequest } from 'next/server';
import connectDB from '@/lib/db';
import User from '@/lib/models/User';
import Lawyer from '@/lib/models/Lawyer';
import Client from '@/lib/models/Client';
import { handleApiError, createSuccessResponse, createErrorResponse } from '@/lib/utils/errorHandler';

// GET current user with their profile (lawyer or client)
export async function GET(req: NextRequest) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return createErrorResponse('Unauthorized', 401);
    }

    await connectDB();

    // Get user
    const user = await User.findOne({ clerkId: userId }).lean();
    
    if (!user) {
      return createErrorResponse('User not found', 404);
    }

    let profile = null;

    // Get role-specific profile
    if (user.role === 'lawyer') {
      profile = await Lawyer.findOne({ clerkId: userId }).lean();
    } else if (user.role === 'client') {
      profile = await Client.findOne({ clerkId: userId }).lean();
    }

    return createSuccessResponse({
      user,
      profile
    });
  } catch (error) {
    return handleApiError(error);
  }
}