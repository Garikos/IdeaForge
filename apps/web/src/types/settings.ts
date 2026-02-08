export interface LlmProviderInfo {
  id: string;
  model: string;
  cost: string;
  speed: string;
  description: string;
  has_api_key: boolean;
  is_active: boolean;
}

export interface LlmSettings {
  current_provider: string;
  providers: LlmProviderInfo[];
}
