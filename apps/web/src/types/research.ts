export interface ResearchRequest {
  query: string;
  sources: string[];
  llm_provider: string;
}

export interface ResearchRun {
  run_id: string;
  status: string;
  query: string;
  sources: string[];
  llm_provider: string;
  created_at: string;
}

export interface BusinessIdea {
  id: number;
  title: string;
  summary: string;
  source: string;
  source_url: string | null;
  business_potential: number | null;
  market_size_score: number | null;
  competition_score: number | null;
  sentiment_score: number | null;
  composite_score: number | null;
  status: string;
  created_at: string;
}

export interface IdeaListResponse {
  items: BusinessIdea[];
  total: number;
}

export interface TokenUsageEvent {
  type: "token_usage";
  run_id: string;
  provider: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  llm_calls: number;
  tpm_limit: number | null;
}
