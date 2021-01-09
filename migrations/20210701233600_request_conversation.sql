CREATE TABLE IF NOT EXISTS request_conversation ( 
    id TEXT PRIMARY KEY NOT NULL,
    created_at TEXT NOT NULL,    -- RFC3339 string
    request_processor TEXT NOT NULL,

    FOREIGN KEY(request_processor) REFERENCES request_processor(id)
);

CREATE TABLE IF NOT EXISTS conversation_audit_log (
    id TEXT PRIMARY KEY NOT NULL,
    created_at TEXT NOT NULL,    -- RFC3339 string
    request_conversation TEXT NOT NULL,
    parent TEXT NULL,
    kind TEXT NOT NULL,
    payload TEXT NOT NULL,

    FOREIGN KEY(request_conversation) REFERENCES request_conversation(id)
    FOREIGN KEY(parent) REFERENCES conversation_audit_log(id)
);

CREATE TABLE IF NOT EXISTS conversation_audit_item_request (
    id TEXT PRIMARY KEY NOT NULL,
    created_at TEXT NOT NULL,    -- RFC3339 string
    request_conversation TEXT NOT NULL,
    payload TEXT NOT NULL,

    FOREIGN KEY(request_conversation) REFERENCES request_conversation(id)
);

CREATE TABLE IF NOT EXISTS conversation_audit_item_log (
    id TEXT PRIMARY KEY NOT NULL,
    created_at TEXT NOT NULL,    -- RFC3339 string
    request_conversation TEXT NOT NULL,
    payload TEXT NOT NULL,

    FOREIGN KEY(request_conversation) REFERENCES request_conversation(id)
);

CREATE TABLE IF NOT EXISTS conversation_audit_item_response (
    id TEXT PRIMARY KEY NOT NULL,
    created_at TEXT NOT NULL,    -- RFC3339 string
    request_conversation TEXT NOT NULL,
    request TEXT NOT NULL,
    payload TEXT NOT NULL,

    FOREIGN KEY(request_conversation) REFERENCES request_conversation(id)
    FOREIGN KEY(request) REFERENCES conversation_audit_item_request(id)
);
