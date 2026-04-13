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

-- Admin user
INSERT INTO users (username, email, password, role)
VALUES ('admin', 'admin@brightup.com', '$2b$12$GT6kkSBCAlnuUrED6NHgqunq0IKbdYf3VyMPdrEhDVhfaG3gI2OyO', 'admin');

-- Sample cards
INSERT INTO cards (title, message, category, created_by) VALUES
('Smile', 'Smile, Smile, Smile!', 'happy', 1),
('Breathe', 'Better days are coming!','calm', 1),
('One Step', 'Focus on just one thing today. Make it count.','productive', 1),
('Be Kind', 'Today is my cup of tea.', 'wellbeing',  1),
('Celebrate You',   'Definitely right now!', 'positivity', 1),
('You Got This', 'You can do it!', 'motivation', 1),
('Take a Break', 'More sweet, must sugar', 'self-care', 1),
('Gratitude', 'Nothing changes if nothing changes.', 'gratitude', 1),
('Believe in Yourself', 'Knock at the door and it will be opened.', 'confidence', 1);
