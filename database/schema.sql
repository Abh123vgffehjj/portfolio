-- ============================================================
-- Abhijeet V S Portfolio - Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE portfolio_db;

-- Admin Users
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Education
CREATE TABLE IF NOT EXISTS education (
    id INT AUTO_INCREMENT PRIMARY KEY,
    degree VARCHAR(200) NOT NULL,
    institution VARCHAR(300) NOT NULL,
    cgpa VARCHAR(20),
    start_year INT,
    end_year INT,
    expected_graduation VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Skills
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    proficiency INT DEFAULT 80 CHECK (proficiency BETWEEN 0 AND 100),
    icon VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    technologies TEXT,
    features TEXT,
    achievement TEXT,
    github_url VARCHAR(500),
    live_url VARCHAR(500),
    image_url VARCHAR(500),
    category VARCHAR(100),
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Certifications
CREATE TABLE IF NOT EXISTS certifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(300) NOT NULL,
    issuer VARCHAR(200) NOT NULL,
    issue_date VARCHAR(50),
    credential_url VARCHAR(500),
    description TEXT,
    badge_color VARCHAR(20) DEFAULT '#E11D2E',
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Achievements
CREATE TABLE IF NOT EXISTS achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    date VARCHAR(100),
    icon VARCHAR(100) DEFAULT 'trophy',
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contacts (messages from visitors)
CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Visitors (analytics)
CREATE TABLE IF NOT EXISTS visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(50),
    user_agent TEXT,
    page VARCHAR(200) DEFAULT '/',
    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resume Uploads
CREATE TABLE IF NOT EXISTS resume_uploads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(300) NOT NULL,
    original_filename VARCHAR(300),
    file_size INT,
    parsed BOOLEAN DEFAULT FALSE,
    parse_status VARCHAR(50) DEFAULT 'pending',
    parse_log TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profile (hero/about section)
CREATE TABLE IF NOT EXISTS profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(200),
    subtitle VARCHAR(300),
    summary TEXT,
    email VARCHAR(200),
    linkedin VARCHAR(500),
    github VARCHAR(500),
    animated_roles TEXT COMMENT 'JSON array of roles',
    resume_filename VARCHAR(300),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_skills_category ON skills(category);
CREATE INDEX idx_projects_featured ON projects(is_featured);
CREATE INDEX idx_contacts_read ON contacts(is_read);
CREATE INDEX idx_visitors_date ON visitors(visited_at);
