import { auth } from '@clerk/nextjs/server';
import { NextRequest } from 'next/server';
import connectDB from '@/lib/db';
import Lawyer from '@/lib/models/Lawyer';
import User from '@/lib/models/User';
import { handleApiError, createSuccessResponse, createErrorResponse } from '@/lib/utils/errorHandler';

// GET single lawyer by ID
export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    await connectDB();

    const lawyer = await Lawyer.findById(params.id)
      .populate('userId', 'firstName lastName email profileImage phone')
      .lean();

    if (!lawyer) {
      return createErrorResponse('Lawyer not found', 404);
    }

    return createSuccessResponse(lawyer);
  } catch (error) {
    return handleApiError(error);
  }
}

// PATCH - Update lawyer profile
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

    const lawyer = await Lawyer.findById(params.id);

    if (!lawyer) {
      return createErrorResponse('Lawyer not found', 404);
    }

    // Check if user owns this profile
    if (lawyer.clerkId !== userId) {
      return createErrorResponse('Forbidden', 403);
    }

    const body = await req.json();

    // Update lawyer profile
    const updatedLawyer = await Lawyer.findByIdAndUpdate(
      params.id,
      { $set: body },
      { new: true, runValidators: true }
    ).populate('userId', 'firstName lastName email profileImage');

    return createSuccessResponse(updatedLawyer, 'Profile updated successfully');
  } catch (error) {
    return handleApiError(error);
  }
}

// DELETE - Deactivate lawyer profile
export async function DELETE(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return createErrorResponse('Unauthorized', 401);
    }

    await connectDB();

    const lawyer = await Lawyer.findById(params.id);

    if (!lawyer) {
      return createErrorResponse('Lawyer not found', 404);
    }

    // Check if user owns this profile
    if (lawyer.clerkId !== userId) {
      return createErrorResponse('Forbidden', 403);
    }

    // Deactivate instead of delete
    lawyer.isActive = false;
    await lawyer.save();

    return createSuccessResponse(null, 'Profile deactivated successfully');
  } catch (error) {
    return handleApiError(error);
  }
}