DROP TABLE IF EXISTS users;

CREATE TABLE users (username CHAR[8] NOT NULL PRIMARY KEY, 
                    security_level INT CHECK(3 >= security_level >= 1) NOT NULL,
                    one_time_id TEXT NOT NULL,
                    ip_address TEXT,
                    public_key TEXT,
                    token TEXT,
                    symmetric_key TEXT,
                    challenge TEXT,
                    challenge_timeout DATE
            );
