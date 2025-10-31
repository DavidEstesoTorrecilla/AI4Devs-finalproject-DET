// Shared TypeScript types between backend and frontend

// User types
export enum UserRole {
  ADMIN = 'ADMIN',
  SUPERVISOR = 'SUPERVISOR',
  TECHNICIAN = 'TECHNICIAN',
  OPERATOR = 'OPERATOR',
}

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

// Machine types
export enum MachineStatus {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  MAINTENANCE = 'MAINTENANCE',
  ERROR = 'ERROR',
}

export interface Machine {
  id: string;
  code: string;
  name: string;
  model?: string;
  manufacturer?: string;
  location?: string;
  zone?: string;
  line?: string;
  status: MachineStatus;
  description?: string;
  lastHeartbeat?: Date;
  ipAddress?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Alert types
export enum AlertType {
  WARNING = 'WARNING',
  ERROR = 'ERROR',
  CRITICAL = 'CRITICAL',
  INFO = 'INFO',
}

export enum AlertStatus {
  OPEN = 'OPEN',
  IN_PROGRESS = 'IN_PROGRESS',
  RESOLVED = 'RESOLVED',
  CLOSED = 'CLOSED',
}

export interface Alert {
  id: string;
  machineId: string;
  userId?: string;
  type: AlertType;
  status: AlertStatus;
  severity: number; // 1-5
  title: string;
  description: string;
  acknowledgedAt?: Date;
  acknowledgedBy?: string;
  resolvedAt?: Date;
  resolvedBy?: string;
  createdAt: Date;
  updatedAt: Date;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role?: UserRole;
}

// Machine metrics types
export interface MachineMetric {
  id: string;
  machineId: string;
  temperature?: number;
  vibration?: number;
  pressure?: number;
  speed?: number;
  power?: number;
  timestamp: Date;
}

// WebSocket event types
export enum WebSocketEvent {
  MACHINE_UPDATE = 'machine:update',
  ALERT_CREATED = 'alert:created',
  ALERT_UPDATED = 'alert:updated',
  METRIC_UPDATE = 'metric:update',
}

export interface WebSocketMessage<T = any> {
  event: WebSocketEvent;
  data: T;
  timestamp: Date;
}
