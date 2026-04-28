// API Response Types
export interface TenantLeadResponse {
  id: number;
  full_name: string;
  phone_number: string;
  email?: string;
  location_preference: string;
  budget_min?: number;
  budget_max: number;
  property_type: string;
  move_in_date: string;
  lead_score: number;
  status: string;
  created_at: string;
  updated_at: string;
}

// Form Data Type (what we collect from user)
export interface LeadFormData {
  fullName: string;
  phoneNumber: string;
  email: string;
  locations: string[]; // Array of selected locations
  propertyType: string;
  budgetMin: string;
  budgetMax: string;
  moveInDate: string;
}

// API Request Payload
export interface TenantLeadRequest {
  full_name: string;
  phone_number: string;
  email?: string;
  location_preference: string; // Comma-separated: "Lekki,Ajah,Yaba"
  budget_min?: number;
  budget_max: number;
  property_type: string;
  move_in_date: string;
}

// API Error Response
export interface ApiError {
  detail?: string;
  message?: string;
  code?: string;
}
