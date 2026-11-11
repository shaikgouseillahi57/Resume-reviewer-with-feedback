-- =========================================================================
-- Supabase Schema for AI Resume Reviewer & Feedback Platform (Hardened)
-- Run this in your Supabase Project -> SQL Editor -> Click 'Run'
-- =========================================================================

-- 1. Create resume_reviews table with user ownership tracking
CREATE TABLE IF NOT EXISTS public.resume_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    filename TEXT,
    target_role TEXT,
    predicted_category TEXT,
    overall_score NUMERIC,
    detected_skills JSONB DEFAULT '[]'::jsonb,
    missing_skills JSONB DEFAULT '[]'::jsonb,
    strengths JSONB DEFAULT '[]'::jsonb,
    weaknesses JSONB DEFAULT '[]'::jsonb,
    recommendations JSONB DEFAULT '[]'::jsonb,
    bullet_rewrites JSONB DEFAULT '[]'::jsonb,
    format_analysis JSONB DEFAULT '{}'::jsonb,
    raw_text TEXT
);

-- 2. Create indices for fast queries
CREATE INDEX IF NOT EXISTS idx_resume_reviews_created_at ON public.resume_reviews (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_resume_reviews_user_id ON public.resume_reviews (user_id);

-- 3. Enable Row Level Security (RLS)
ALTER TABLE public.resume_reviews ENABLE ROW LEVEL SECURITY;

-- 4. Drop legacy insecure policies
DROP POLICY IF EXISTS "Allow public read access" ON public.resume_reviews;
DROP POLICY IF EXISTS "Allow public insert access" ON public.resume_reviews;
DROP POLICY IF EXISTS "Users can read own reviews or anonymous reviews" ON public.resume_reviews;
DROP POLICY IF EXISTS "Users can insert reviews" ON public.resume_reviews;
DROP POLICY IF EXISTS "Users can delete own reviews" ON public.resume_reviews;

-- 5. Hardened RLS Policies
-- SELECT: Users can only read their own reviews; if unauthenticated, only unowned (guest) reviews can be read
CREATE POLICY "Users can read own reviews or anonymous reviews"
ON public.resume_reviews
FOR SELECT
TO anon, authenticated
USING (
    (auth.uid() IS NOT NULL AND user_id = auth.uid()) OR
    (auth.uid() IS NULL AND user_id IS NULL)
);

-- INSERT: Authenticated users insert with their own user_id; anonymous users insert with user_id NULL
CREATE POLICY "Users can insert reviews"
ON public.resume_reviews
FOR INSERT
TO anon, authenticated
WITH CHECK (
    (auth.uid() IS NOT NULL AND (user_id IS NULL OR user_id = auth.uid())) OR
    (auth.uid() IS NULL AND user_id IS NULL)
);

-- UPDATE: Users can only update their own records
CREATE POLICY "Users can update own reviews"
ON public.resume_reviews
FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- DELETE: Users can only delete their own records
CREATE POLICY "Users can delete own reviews"
ON public.resume_reviews
FOR DELETE
TO authenticated
USING (auth.uid() = user_id);
