CREATE DATABASE IF NOT EXISTS brightup;
USE brightup;

CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE mood_ratings (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    rating      TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    note        TEXT,                           -- optional personal note
    rated_at    DATE NOT NULL DEFAULT (CURRENT_DATE),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_day (user_id, rated_at)  -- only 1 rating per day
);


CREATE TABLE cards (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    message     TEXT NOT NULL,                  -- motivational message
    category    VARCHAR(50),                    -- e.g. 'motivation', 'calm', 'energy'
    is_active   BOOLEAN DEFAULT TRUE,
    created_by  INT,                            -- admin user id
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE user_daily_cards (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    card_id     INT NOT NULL,
    assigned_at DATE NOT NULL DEFAULT (CURRENT_DATE),

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_card_day (user_id, assigned_at)  -- only 1 card per day
);

-- Admin user (password: "admin123" — change this in production!)
INSERT INTO users (username, email, password, role)
VALUES ('admin', 'admin@brightup.com', '$2b$12$placeholder_hashed_password', 'admin');

-- Sample cards
INSERT INTO cards (title, message, category, created_by) VALUES
('Start Small',     'You don\'t have to be great to start, but you have to start to be great.', 'motivation', 1),
('Breathe',         'Take 3 deep breaths. You\'ve got this.',                                   'calm',       1),
('One Step',        'Focus on just one thing today. Make it count.',                            'focus',      1),
('Be Kind',         'Say something kind to someone today — including yourself.',                'wellbeing',  1),
('Celebrate You',   'You made it through yesterday. That already matters.',                     'positivity', 1);