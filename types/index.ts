export interface User {
  id: number;
  nickname: string;
  email?: string;
  created_at: string;
  updated_at: string;
}

export interface Post {
  id: number;
  title: string;
  content?: string;
  author: User;
  created_at: string;
  updated_at: string;
  comments_count: number;
}

export interface Comment {
  id: number;
  content: string;
  author: User;
  post_id: number;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  items?: T[];
  posts?: T[];
  comments?: T[];
  users?: T[];
  total: number;
  pages: number;
  current_page: number;
  per_page: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface AuthResponse {
  message: string;
  access_token: string;
  user: User;
}

export interface ApiError {
  error: string;
}

export interface CreatePostData {
  title: string;
  content: string;
}

export interface UpdatePostData {
  title?: string;
  content?: string;
}

export interface CreateCommentData {
  content: string;
  post_id: number;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface SignupData {
  nickname: string;
  email: string;
  password: string;
} 