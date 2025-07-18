CREATE DATABASE IF NOT EXISTS matrimony;
USE matrimony;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender ENUM('male','female','other'),
    age INT,
    location VARCHAR(100),
    religion VARCHAR(50),
    language_preference VARCHAR(50),
    bio TEXT,
    profile_photo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
