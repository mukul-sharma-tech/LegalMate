import { auth } from '@clerk/nextjs/server';
import { NextRequest } from 'next/server';
import connectDB from '@/lib/db';
import Booking from '@/lib/models/Booking';
import User from '@/lib/models/User';
import Lawyer from '@/lib/models/Lawyer';
import { handleApiError, createSuccessResponse, createErrorResponse } from '@/lib/utils/errorHandler';

// GET all bookings for current user
export async function GET(req: NextRequest) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return createErrorResponse('Unauthorized', 401);
    }

    await connectDB();

    const { searchParams } = new URL(req.url);
    const status = searchParams.get('status');

    // Get current user
    const user = await User.findOne({ clerkId: userId });
    
    if (!user) {
      return createErrorResponse('User not found', 404);
    }

    // Build query based on user role
    let query: any = {};
    
    if (user.role === 'client') {
      query.clientId = user._id;
    } else if (user.role === 'lawyer') {
      const lawyer = await Lawyer.findOne({ clerkId: userId });
      if (!lawyer) {
        return createErrorResponse('Lawyer profile not found', 404);
      }
      query.lawyerId = lawyer._id;
    }

    if (status) {
      query.status = status;
    }

    const bookings = await Booking.find(query)
      .populate('clientId', 'firstName lastName email profileImage')
      .populate({
        path: 'lawyerId',
        populate: {
          path: 'userId',
          select: 'firstName lastName email profileImage'
        }
      })
      .sort({ createdAt: -1 })
      .lean();

    return createSuccessResponse(bookings);
  } catch (error) {
    return handleApiError(error);
  }
}

// POST - Create new booking
export async function POST(req: NextRequest) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return createErrorResponse('Unauthorized', 401);
    }

    await connectDB();

    const body = await req.json();
    const {
      lawyerId,
      sessionType,
      durationType,
      preferredDate,
      preferredTime,
      issueDescription,
      clientNotes
    } = body;

    // Get current user (must be client)
    const user = await User.findOne({ clerkId: userId });
    
    if (!user) {
      return createErrorResponse('User not found', 404);
    }

    if (user.role !== 'client') {
      return createErrorResponse('Only clients can create bookings', 403);
    }

    // Get lawyer
    const lawyer = await Lawyer.findById(lawyerId);
    
    if (!lawyer) {
      return createErrorResponse('Lawyer not found', 404);
    }

    if (!lawyer.isActive) {
      return createErrorResponse('Lawyer is not available', 400);
    }

    // Calculate amount based on duration
    const amount = durationType === 'half-hour' 
      ? lawyer.fees.perHalfHour 
      : lawyer.fees.perHour;

    // Create booking
    const booking = await Booking.create({
      clientId: user._id,
      lawyerId: lawyer._id,
      sessionType,
      durationType,
      preferredDate: new Date(preferredDate),
      preferredTime,
      issueDescription,
      clientNotes,
      amount,
      currency: lawyer.fees.currency,
      status: 'pending',
      paymentStatus: 'pending',
      requestedAt: new Date()
    });

    // Populate for response
    await booking.populate([
      { path: 'clientId', select: 'firstName lastName email' },
      { 
        path: 'lawyerId',
        populate: { path: 'userId', select: 'firstName lastName email' }
      }
    ]);

    return createSuccessResponse(
      booking,
      'Booking created successfully. Waiting for lawyer approval.',
      201
    );
  } catch (error) {
    return handleApiError(error);
  }
}