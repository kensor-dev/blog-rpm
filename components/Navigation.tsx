'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';

export default function Navigation() {
  const { user, logout, isLoading } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <nav className="bg-white shadow-lg border-b">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          {/* Logo/Brand */}
          <Link href="/" className="text-2xl font-bold text-blue-600 hover:text-blue-700">
            Blog RPM
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-6">
            <Link 
              href="/" 
              className="text-gray-600 hover:text-blue-600 transition-colors"
            >
              Home
            </Link>

            {!isLoading && (
              <>
                {user ? (
                  <>
                    {/* Authenticated user menu */}
                    <Link 
                      href="/posts/new" 
                      className="text-gray-600 hover:text-blue-600 transition-colors"
                    >
                      Write Post
                    </Link>
                    <Link 
                      href={`/${user.nickname}`} 
                      className="text-gray-600 hover:text-blue-600 transition-colors"
                    >
                      My Blog
                    </Link>
                    <div className="flex items-center space-x-4">
                      <span className="text-gray-700">
                        Welcome, <strong>{user.nickname}</strong>
                      </span>
                      <button 
                        onClick={handleLogout}
                        className="btn-secondary text-sm"
                      >
                        Logout
                      </button>
                    </div>
                  </>
                ) : (
                  <>
                    {/* Guest user menu */}
                    <Link 
                      href="/auth/login" 
                      className="text-gray-600 hover:text-blue-600 transition-colors"
                    >
                      Login
                    </Link>
                    <Link 
                      href="/auth/signup" 
                      className="btn-primary text-sm"
                    >
                      Sign Up
                    </Link>
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
} 