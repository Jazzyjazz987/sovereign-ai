-- Initialize LangGraph state tables
CREATE SCHEMA IF NOT EXISTS langgraph;

CREATE TABLE IF NOT EXISTS langgraph.graph_state (
    id SERIAL PRIMARY KEY,
    thread_id VARCHAR(255) NOT NULL,
    checkpoint_ns VARCHAR(255),
    checkpoint_id VARCHAR(36),
    metadata JSONB,
    values JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_thread_id ON langgraph.graph_state(thread_id);
CREATE INDEX idx_checkpoint_id ON langgraph.graph_state(checkpoint_id);

-- Initialize LiteLLM logging tables
CREATE TABLE IF NOT EXISTS litellm_logs (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(255),
    model_name VARCHAR(255),
    user_id VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_model_name ON litellm_logs(model_name);
