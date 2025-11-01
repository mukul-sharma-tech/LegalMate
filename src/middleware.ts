import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/lawyers',
  '/lawyers/(.*)',
  '/api/webhooks/(.*)',
  '/api/auth/onboarding(.*)', // Allow onboarding API - FIXED PATH
  '/api/user/onboarding(.*)' // Keep both for compatibility
]);

const isOnboardingRoute = createRouteMatcher(['/onboarding']);

export default clerkMiddleware(async (auth, req) => {
  const { userId, sessionClaims } = await auth();

  // Allow public routes
  if (isPublicRoute(req)) {
    return NextResponse.next();
  }

  // Redirect unauthenticated users to sign-in
  if (!userId) {
    const signInUrl = new URL('/sign-in', req.url);
    signInUrl.searchParams.set('redirect_url', req.url);
    return NextResponse.redirect(signInUrl);
  }

  // Allow onboarding route for authenticated users
  if (isOnboardingRoute(req)) {
    return NextResponse.next();
  }

  // Check if user has completed onboarding using metadata
  // We'll use Clerk's public metadata to store onboarding status
  const metadata = sessionClaims?.metadata as { onboardingCompleted?: boolean } | undefined;
  
  if (!metadata?.onboardingCompleted) {
    // Redirect to onboarding if not completed
    return NextResponse.redirect(new URL('/onboarding', req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};