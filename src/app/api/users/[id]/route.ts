import { auth } from '@clerk/nextjs/server';
import { NextRequest } from 'next/server';
import connectDB from '@/lib/db';
import User from '@/lib/models/User';
import { handleApiError, createSuccessResponse, createErrorResponse } from '@/lib/utils/errorHandler';

// GET user by ID
export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    await connectDB();

    const user = await User.findById(params.id).select('-clerkId').lean();
    
    if (!user) {
      return createErrorResponse('User not found', 404);
    }

    return createSuccessResponse(user);
  } catch (error) {
    return handleApiError(error);
  }
}

// PATCH - Update user profile
export async function PATCH(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return createErrorResponse('Unauthorized', 401);
    }

    await connectDB();

    // Get user
    const user = await User.findById(params.id);

    if (!user) {
      return createErrorResponse('User not found', 404);
    }

    // Check if user owns this profile
    if (user.clerkId !== userId) {
      return createErrorResponse('Forbidden', 403);
    }

    const body = await req.json();

    // Only allow certain fields to be updated
    const allowedUpdates = ['firstName', 'lastName', 'phone', 'profileImage'];
    const updates: any = {};

    for (const key of allowedUpdates) {
      if (body[key] !== undefined) {
        updates[key] = body[key];
      }
    }

    const updatedUser = await User.findByIdAndUpdate(
      params.id,
      { $set: updates },
      { new: true, runValidators: true }
    ).select('-clerkId');

    return createSuccessResponse(updatedUser, 'Profile updated successfully');
  } catch (error) {
    return handleApiError(error);
  }
}