export interface Plan {
  id?: number;       // optional if your API returns IDs
  name: string;
  price: string;
  data?: string;     // optional
  [key: string]: any; // for extra fields from API
}
