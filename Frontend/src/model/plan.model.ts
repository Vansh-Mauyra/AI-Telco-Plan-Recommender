export interface Plan {
  plan_id: number;
  plan_name: string;       // matches backend
  monthly_fee: number;     // matches backend
  validity_days: number;
  plan_type: 'prepaid' | 'postpaid' | 'enterprise';
  data_gb?: number;
  daily_data_gb?: number;
  voice_minutes?: number;
  sms_count?: number;
  roaming_included?: boolean;
  international_roaming?: boolean;
  network_type?: '4G' | '5G' | 'Both';
  contract_months?: number;
  is_active?: boolean;
}
