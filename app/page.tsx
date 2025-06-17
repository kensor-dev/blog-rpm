'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { postsApi } from '@/lib/api';
import type { Post, PaginatedResponse } from '@/types';

export default function HomePage() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [pagination, setPagination] = useState<PaginatedResponse<Post> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    fetchPosts(currentPage);
  }, [currentPage]);

  const fetchPosts = async (page: number) => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await postsApi.getPosts(page, 10);
      setPosts(response.posts || []);
      setPagination(response);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load posts');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Blog RPM
        </h1>
        <p className="text-lg text-gray-600">
          Discover amazing stories and insights from our community of writers.
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="error-message mb-6">
          {error}
        </div>
      )}

      {/* Posts List */}
      {posts.length === 0 ? (
        <div className="text-center py-12">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            No posts yet
          </h2>
          <p className="text-gray-600 mb-6">
            Be the first to share your story with the community!
          </p>
          <Link href="/auth/signup" className="btn-primary">
            Get Started
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {posts.map((post) => (
            <article key={post.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                    <Link 
                      href={`/posts/${post.id}`}
                      className="hover:text-blue-600 transition-colors"
                    >
                      {post.title}
                    </Link>
                  </h2>
                  
                  <div className="flex items-center text-sm text-gray-500 space-x-4">
                    <span>
                      By{' '}
                      <Link 
                        href={`/${post.author.nickname}`}
                        className="text-blue-600 hover:text-blue-700 font-medium"
                      >
                        {post.author.nickname}
                      </Link>
                    </span>
                    <span>{formatDate(post.created_at)}</span>
                    <span>{formatTime(post.created_at)}</span>
                    <span>{post.comments_count} comments</span>
                  </div>
                </div>
              </div>

              {/* Post Preview */}
              {post.content && (
                <div className="text-gray-700 mb-4">
                  <p className="line-clamp-3">
                    {post.content.substring(0, 200)}
                    {post.content.length > 200 && '...'}
                  </p>
                </div>
              )}

              <div className="flex justify-between items-center">
                <Link 
                  href={`/posts/${post.id}`}
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  Read more →
                </Link>
              </div>
            </article>
          ))}
        </div>
      )}

      {/* Pagination */}
      {pagination && pagination.pages > 1 && (
        <div className="flex justify-center items-center space-x-4 mt-8">
          <button
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={!pagination.has_prev}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          <span className="text-gray-600">
            Page {pagination.current_page} of {pagination.pages}
          </span>
          
          <button
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={!pagination.has_next}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
} 