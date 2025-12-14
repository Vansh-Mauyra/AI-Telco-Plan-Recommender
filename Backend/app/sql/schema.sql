-- =============================
-- Telco AI Recommender Database Schema
-- =============================

--CREATE EXTENSION IF NOT EXISTS vector;   -- only needed if using RAG embeddings

-- =============================
-- 1. CARRIER TABLE
-- =============================
CREATE TABLE carrier (
    carrier_id SERIAL PRIMARY KEY,
    carrier_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    website TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_carrier_name ON carrier(carrier_name);


-- =============================
-- 2. TELCO PLANS
-- =============================
CREATE TABLE telco_plan (
    plan_id SERIAL PRIMARY KEY,
    carrier_id INT REFERENCES carrier(carrier_id) ON DELETE CASCADE,
    plan_name VARCHAR(100) NOT NULL,
    plan_code VARCHAR(30) UNIQUE,
    monthly_fee NUMERIC(10,2) NOT NULL CHECK(monthly_fee >= 0),
    validity_days INT NOT NULL CHECK(validity_days > 0),
    plan_type VARCHAR(20) CHECK(plan_type IN ('prepaid','postpaid','enterprise')),
    -- allowances
    data_gb NUMERIC(10,2) CHECK(data_gb >= 0),
    daily_data_gb NUMERIC(10,2) CHECK(daily_data_gb >= 0),
    voice_minutes INT CHECK(voice_minutes >= 0),
    sms_count INT CHECK(sms_count >= 0),
    roaming_included BOOLEAN DEFAULT FALSE,
    international_roaming BOOLEAN DEFAULT FALSE,
    network_type VARCHAR(10) CHECK(network_type IN ('4G','5G','Both')),
    contract_months INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_plan_carrier ON telco_plan(carrier_id);
CREATE INDEX idx_plan_fee ON telco_plan(monthly_fee);
CREATE INDEX idx_plan_data ON telco_plan(data_gb);
CREATE INDEX idx_plan_daily_data ON telco_plan(daily_data_gb);
CREATE INDEX idx_plan_voice_minutes ON telco_plan(voice_minutes);
CREATE INDEX idx_plan_active ON telco_plan(is_active);


-- =============================
-- 3. ADDON PLANS
-- =============================
CREATE TABLE addon (
    addon_id SERIAL PRIMARY KEY,
    carrier_id INT REFERENCES carrier(carrier_id),
    addon_name TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL CHECK(price >= 0),
    data_gb NUMERIC(10,2) DEFAULT 0,
    voice_minutes INT DEFAULT 0,
    sms_count INT DEFAULT 0,
    validity_days INT CHECK(validity_days > 0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_addon_carrier ON addon(carrier_id);
CREATE INDEX idx_addon_price ON addon(price);


-- =============================
-- 4. CUSTOMER PROFILE
-- =============================
CREATE TABLE customer_profile (
    customer_id BIGSERIAL PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE,
    email VARCHAR(100),
    name VARCHAR(100),
    current_carrier_id INT REFERENCES carrier(carrier_id),
    current_plan_id INT REFERENCES telco_plan(plan_id),
    avg_monthly_data_gb NUMERIC(10,2),
    avg_voice_minutes INT,
    avg_sms INT,
    budget NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_customer_carrier ON customer_profile(current_carrier_id);
CREATE INDEX idx_customer_plan ON customer_profile(current_plan_id);
CREATE INDEX idx_customer_budget ON customer_profile(budget);


-- =============================
-- 5. USAGE HISTORY
-- =============================
CREATE TABLE usage_history (
    usage_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customer_profile(customer_id) ON DELETE CASCADE,
    month DATE NOT NULL,
    data_gb NUMERIC(10,2),
    voice_minutes INT,
    sms INT,
    roaming_charges NUMERIC(10,2) DEFAULT 0,
    international_usage BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_usage_customer ON usage_history(customer_id);
CREATE INDEX idx_usage_month ON usage_history(month);


-- =============================
-- 6. RECOMMENDATION LOGS
-- =============================
CREATE TABLE recommendation_log (
    rec_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customer_profile(customer_id),
    input_query TEXT NOT NULL,
    intent VARCHAR(50),
    extracted_constraints JSONB,
    result_plans JSONB,
    chosen_plan_id INT REFERENCES telco_plan(plan_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_rec_customer ON recommendation_log(customer_id);
CREATE INDEX idx_rec_created ON recommendation_log(created_at);
CREATE INDEX idx_rec_intent ON recommendation_log(intent);


-- =============================
-- 7. OPTIONAL: RAG DOCUMENT STORE
-- =============================
-- CREATE TABLE telco_documents (
--     doc_id BIGSERIAL PRIMARY KEY,
--     carrier_id INT REFERENCES carrier(carrier_id),
--     title TEXT,
--     content TEXT NOT NULL,
--     embedding VECTOR(1536),
--     metadata JSONB,
--     created_at TIMESTAMP DEFAULT NOW()
-- );

-- CREATE INDEX idx_doc_embedding
-- ON telco_documents
-- USING ivfflat (embedding vector_cosine_ops);
