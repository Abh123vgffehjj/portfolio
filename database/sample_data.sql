-- ============================================================
-- Abhijeet V S Portfolio - Sample / Seed Data
-- ============================================================
USE portfolio_db;

-- Admin user (password: Admin@123 - change immediately after setup!)
-- Hash generated with werkzeug.security.generate_password_hash('Admin@123')
-- NOTE: The env-var fallback (ADMIN_USERNAME / ADMIN_PASSWORD) also works for login
INSERT INTO admin_users (username, password_hash) VALUES
('admin', 'scrypt:32768:8:1$mTjVLwKfJEf5MzEP$5fbdf7799bc5be11da184a06405e39936e416856780b4ef6976122f30f89d353bbdeb939cbd3b6cdab23bd1b3892e783c93cab0bff0d5058b5790c879311310f');

-- Profile
INSERT INTO profile (full_name, role, subtitle, summary, email, linkedin, github, animated_roles, resume_filename) VALUES
('Abhijeet V S',
 'AI & IoT Developer',
 'Computer Science Engineering Student',
 'Motivated Computer Science and Engineering student with a strong foundation in Artificial Intelligence, Data Analytics, IoT systems, and Software Development. Experienced in building real-time monitoring solutions, embedded systems, and data-driven applications. Passionate about creating technology that solves real-world problems.',
 'abhijeetvs@email.com',
 'https://linkedin.com/in/abhijeetvs2308',
 'https://github.com/Abh123vgffehjj',
 '["AI Developer", "IoT Innovator", "Data Analytics Enthusiast", "Full-Stack Developer"]',
 'resume.pdf');

-- Education
INSERT INTO education (degree, institution, cgpa, start_year, expected_graduation, description) VALUES
('Bachelor of Engineering (Computer Science and Engineering)',
 'Loyola-ICAM College of Engineering and Technology (LICET)',
 '8.54 / 10',
 2024,
 '2028',
 'Specializing in Artificial Intelligence, IoT, Data Analytics, and Software Development. Active participant in technical events and innovation competitions.');

-- Skills
INSERT INTO skills (name, category, proficiency, icon) VALUES
-- Programming Languages
('Python', 'Programming', 90, 'code'),
('Java', 'Programming', 82, 'code'),
('C', 'Programming', 75, 'code'),
('Arduino C/C++', 'Programming', 85, 'cpu'),
-- Web Technologies
('HTML5', 'Web', 88, 'globe'),
('CSS3', 'Web', 85, 'palette'),
('JavaScript', 'Web', 80, 'zap'),
('Flask', 'Web', 82, 'server'),
-- Databases
('MySQL', 'Databases', 80, 'database'),
('MongoDB', 'Databases', 75, 'database'),
-- AI & Analytics
('Data Analysis', 'AI & Analytics', 85, 'bar-chart'),
('Risk Profiling', 'AI & Analytics', 78, 'shield'),
('Anomaly Detection', 'AI & Analytics', 80, 'activity'),
('Predictive Analytics', 'AI & Analytics', 78, 'trending-up'),
('Data Storytelling', 'AI & Analytics', 82, 'pie-chart'),
-- Technologies
('IoT', 'Technologies', 88, 'wifi'),
('Embedded Systems', 'Technologies', 85, 'cpu'),
('BLE', 'Technologies', 78, 'bluetooth'),
('OOP', 'Technologies', 85, 'layers'),
('MVC Architecture', 'Technologies', 80, 'layout'),
('Design Patterns', 'Technologies', 78, 'grid');

-- Projects
INSERT INTO projects (title, description, technologies, features, achievement, category, is_featured, display_order) VALUES
('Mine Safety Smart Helmet',
 'An IoT-based smart helmet system designed to monitor the health and safety of mine workers in real-time. The system detects dangerous conditions, tracks vital signs, and provides instant alerts to prevent accidents in hazardous mining environments.',
 'ESP32,Python,Flask,MongoDB Atlas,HTML,CSS,JavaScript,Chart.js',
 'Real-time health monitoring,Fall detection with instant alerts,Safety score computation,Environmental hazard detection,Live dashboard with analytics,Historical data visualization,Multi-worker monitoring',
 'Presented at PALS innoWAH! Finals and IIT Madras',
 'IoT',
 TRUE,
 1),

('Smart Walkers – IoT-Based Smart Health Monitoring Footwear',
 'Intelligent footwear equipped with multiple sensors to monitor the health and mobility of users, particularly elderly individuals. Provides real-time data on gait, heart rate, and location while detecting falls and sending emergency alerts.',
 'ESP32,MPU6050,Pulse Sensor,GPS Module,Arduino C/C++,BLE',
 'Real-time GPS tracking,Heart-rate monitoring,Gait analysis and pattern detection,Fall detection with emergency alerts,BLE connectivity,Caregiver mobile notifications,Battery-efficient design',
 'Presented at STROM 2K24',
 'IoT',
 TRUE,
 2),

('Smart Music Player',
 'A feature-rich music player application built with Java Swing, implementing multiple design patterns for scalable and maintainable code. Features mood-based recommendations and smart playlist management.',
 'Java,Swing GUI,MVC Architecture,Design Patterns',
 'Mood-based music recommendations,Trending playlist generation,Singleton Pattern for audio engine,Factory Pattern for playlist creation,Strategy Pattern for recommendation algorithms,Observer Pattern for UI updates,Facade Pattern for media controls',
 NULL,
 'Software',
 FALSE,
 3);

-- Certifications
INSERT INTO certifications (name, issuer, issue_date, description, badge_color, display_order) VALUES
('GenAI Powered Data Analytics Job Simulation', 'Forage', '2024', 'Completed a comprehensive job simulation focused on applying Generative AI techniques to real-world data analytics problems.', '#E11D2E', 1),
('Programming in Java', 'NPTEL', '2024', 'Elite certification in Java programming from NPTEL, covering advanced OOP concepts, data structures, and design patterns.', '#FF3040', 2),
('German I', 'NPTEL', '2024', 'Elite certification in German language fundamentals from NPTEL, demonstrating multilingual communication skills.', '#CC1525', 3);

-- Achievements
INSERT INTO achievements (title, description, date, icon, display_order) VALUES
('Finalist – PALS innoWAH! 2025–26', 'Selected as a finalist in the prestigious PALS innoWAH! innovation competition, competing against top engineering students from across India.', '2025', 'award', 1),
('Presented at IIT Madras', 'Presented the Mine Safety Smart Helmet project at IIT Madras, one of India''s premier engineering institutions, to an audience of researchers and industry experts.', '2025', 'star', 2),
('Startup Pitch Competition Participant', 'Participated in a startup pitch competition, presenting a business case for IoT-based safety solutions to investors and industry mentors.', '2024', 'briefcase', 3),
('Presented at STROM 2K24', 'Presented Smart Walkers – IoT-Based Smart Health Monitoring Footwear at STROM 2K24, receiving recognition for innovation in healthcare technology.', '2024', 'trophy', 4);
