import axios from 'axios';
import { TenantLeadRequest, TenantLeadResponse, ApiError } from '../types/types';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Submit tenant lead form to backend
 * POST /leads endpoint
 */
export const submitTenantLead = async (
  formData: TenantLeadRequest
): Promise<{ success: boolean; data?: TenantLeadResponse; error?: ApiError }> => {
  try {
    const response = await api.post<TenantLeadResponse>('/leads/', formData);
    return { success: true, data: response.data };
  } catch (err: any) {
    // Handle specific error responses
    if (err.response?.status === 409) {
      return {
        success: false,
        error: {
          code: 'DUPLICATE_PHONE',
          message: 'This phone number is already registered. Please use a different number.',
        },
      };
    }

    if (err.response?.status === 422) {
      return {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: err.response?.data?.detail || 'Please check your form and try again.',
        },
      };
    }

    return {
      success: false,
      error: {
        code: 'NETWORK_ERROR',
        message: 'Network error. Please check your connection and try again.',
      },
    };
  }
};

export default api;
