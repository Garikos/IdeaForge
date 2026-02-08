export interface AgentInfo {
  id: string;
  name: string;
  category: string;
  cost: "free" | string;
  description: string;
  limits: string;
  requires_key: string | null;
  enabled: boolean;
  has_api_key: boolean;
}

export interface AgentRunStatus {
  agent_name: string;
  status: "pending" | "running" | "completed" | "failed";
  duration_seconds: number | null;
  result_summary: string | null;
  error_message: string | null;
}
