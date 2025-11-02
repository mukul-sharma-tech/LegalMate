// app/lawyer/profile/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface Education {
  degree: string;
  university: string;
  yearOfGraduation: number;
}

interface LawyerProfile {
  _id: string;
  barRegistrationNumber: string;
  yearsOfExperience: number;
  specializations: string[];
  languagesSpoken: string[];
  education: Education[];
  about: string;
  fees: {
    perHour: number;
    perHalfHour: number;
  };
}

const SPECIALIZATIONS = [
  'Criminal Law',
  'Civil Law',
  'Corporate Law',
  'Family Law',
  'Tax Law',
  'Property Law',
  'Labor Law',
  'Constitutional Law',
  'Intellectual Property',
  'Immigration Law'
];

const LANGUAGES = ['English', 'Hindi', 'Bengali', 'Tamil', 'Telugu', 'Marathi', 'Gujarati', 'Kannada', 'Malayalam', 'Punjabi'];

export default function LawyerProfileEditPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [profile, setProfile] = useState<LawyerProfile | null>(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await fetch('/api/lawyer/profile');
      const data = await response.json();
      if (data.success) {
        setProfile(data.data);
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!profile) return;
    
    setSaving(true);
    try {
      const response = await fetch(`/api/lawyers/${profile._id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile)
      });

      const data = await response.json();

      if (data.success) {
        alert('Profile updated successfully!');
        router.push('/dashboard/lawyer');
      } else {
        alert(data.message || 'Failed to update profile');
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const addEducation = () => {
    if (!profile) return;
    setProfile({
      ...profile,
      education: [...profile.education, { degree: '', university: '', yearOfGraduation: new Date().getFullYear() }]
    });
  };

  const removeEducation = (index: number) => {
    if (!profile) return;
    setProfile({
      ...profile,
      education: profile.education.filter((_, i) => i !== index)
    });
  };

  const updateEducation = (index: number, field: keyof Education, value: any) => {
    if (!profile) return;
    const newEducation = [...profile.education];
    newEducation[index] = { ...newEducation[index], [field]: value };
    setProfile({ ...profile, education: newEducation });
  };

  const toggleSpecialization = (spec: string) => {
    if (!profile) return;
    const specializations = profile.specializations.includes(spec)
      ? profile.specializations.filter(s => s !== spec)
      : [...profile.specializations, spec];
    setProfile({ ...profile, specializations });
  };

  const toggleLanguage = (lang: string) => {
    if (!profile) return;
    const languagesSpoken = profile.languagesSpoken.includes(lang)
      ? profile.languagesSpoken.filter(l => l !== lang)
      : [...profile.languagesSpoken, lang];
    setProfile({ ...profile, languagesSpoken });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <p className="text-gray-500">Failed to load profile</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="bg-black text-white py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <button
            onClick={() => router.push('/dashboard/lawyer')}
            className="text-gray-400 hover:text-white mb-4"
          >
            ← Back to dashboard
          </button>
          <h1 className="text-4xl font-bold mb-2">Edit Profile</h1>
          <p className="text-gray-400">Update your professional information</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Basic Information</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bar Registration Number
                </label>
                <input
                  type="text"
                  value={profile.barRegistrationNumber}
                  onChange={(e) => setProfile({ ...profile, barRegistrationNumber: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Years of Experience
                </label>
                <input
                  type="number"
                  value={profile.yearsOfExperience}
                  onChange={(e) => setProfile({ ...profile, yearsOfExperience: parseInt(e.target.value) })}
                  min="0"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                  required
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                About
              </label>
              <textarea
                value={profile.about}
                onChange={(e) => setProfile({ ...profile, about: e.target.value })}
                rows={6}
                maxLength={1000}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                required
              />
              <p className="text-xs text-gray-500 mt-1">{profile.about.length}/1000 characters</p>
            </div>
          </div>

          {/* Fees */}
          <div className="border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Consultation Fees</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Per Hour (₹)
                </label>
                <input
                  type="number"
                  value={profile.fees.perHour}
                  onChange={(e) => setProfile({ 
                    ...profile, 
                    fees: { ...profile.fees, perHour: parseInt(e.target.value) }
                  })}
                  min="0"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Per Half Hour (₹)
                </label>
                <input
                  type="number"
                  value={profile.fees.perHalfHour}
                  onChange={(e) => setProfile({ 
                    ...profile, 
                    fees: { ...profile.fees, perHalfHour: parseInt(e.target.value) }
                  })}
                  min="0"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                  required
                />
              </div>
            </div>
          </div>

          {/* Specializations */}
          <div className="border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Specializations</h2>
            <p className="text-sm text-gray-600 mb-4">Select all that apply</p>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {SPECIALIZATIONS.map((spec) => (
                <button
                  key={spec}
                  type="button"
                  onClick={() => toggleSpecialization(spec)}
                  className={`px-4 py-2 rounded-lg border transition-colors ${
                    profile.specializations.includes(spec)
                      ? 'border-black bg-black text-white'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  {spec}
                </button>
              ))}
            </div>
          </div>

          {/* Languages */}
          <div className="border border-gray-200 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Languages Spoken</h2>
            <p className="text-sm text-gray-600 mb-4">Select all languages you speak</p>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {LANGUAGES.map((lang) => (
                <button
                  key={lang}
                  type="button"
                  onClick={() => toggleLanguage(lang)}
                  className={`px-4 py-2 rounded-lg border transition-colors ${
                    profile.languagesSpoken.includes(lang)
                      ? 'border-black bg-black text-white'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  {lang}
                </button>
              ))}
            </div>
          </div>

          {/* Education */}
          <div className="border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold">Education</h2>
              <button
                type="button"
                onClick={addEducation}
                className="text-sm text-black hover:underline"
              >
                + Add Education
              </button>
            </div>

            <div className="space-y-4">
              {profile.education.map((edu, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-end mb-3">
                    <button
                      type="button"
                      onClick={() => removeEducation(index)}
                      className="text-sm text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </div>

                  <div className="grid grid-cols-1 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Degree
                      </label>
                      <input
                        type="text"
                        value={edu.degree}
                        onChange={(e) => updateEducation(index, 'degree', e.target.value)}
                        placeholder="e.g., LLB, LLM"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        University
                      </label>
                      <input
                        type="text"
                        value={edu.university}
                        onChange={(e) => updateEducation(index, 'university', e.target.value)}
                        placeholder="University name"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Year of Graduation
                      </label>
                      <input
                        type="number"
                        value={edu.yearOfGraduation}
                        onChange={(e) => updateEducation(index, 'yearOfGraduation', parseInt(e.target.value))}
                        min="1950"
                        max={new Date().getFullYear()}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                        required
                      />
                    </div>
                  </div>
                </div>
              ))}

              {profile.education.length === 0 && (
                <div className="text-center py-8 border border-gray-200 rounded-lg">
                  <p className="text-gray-500 mb-2">No education added</p>
                  <button
                    type="button"
                    onClick={addEducation}
                    className="text-sm text-black hover:underline"
                  >
                    + Add your first education
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Submit */}
          <div className="flex justify-end gap-4">
            <button
              type="button"
              onClick={() => router.push('/dashboard/lawyer')}
              className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 disabled:opacity-50 font-medium"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}