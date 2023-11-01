CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(32) NOT NULL,
  last_name VARCHAR(32),
  email VARCHAR(64) NOT NULL UNIQUE,
  hashed_password VARCHAR(128) NOT NULL,
);

CREATE TABLE movies_shows (
  mov_show_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE reviews (
  review_id INT AUTO_INCREMENT PRIMARY KEY,
  mov_show_id INT NOT NULL,
  FOREIGN KEY (mov_show_id) REFERENCES movies_shows(mov_show_id)
);

CREATE TABLE locations (
  locations_id INT AUTO_INCREMENT PRIMARY KEY,
  mov_show_id INT NOT NULL,
  FOREIGN KEY (mov_show_id) REFERENCES movies_shows(mov_show_id)
);

CREATE TABLE shares (
  share_id INT AUTO_INCREMENT PRIMARY KEY,
  review_id INT NOT NULL,
  FOREIGN KEY (review_id) REFERENCES reviews(review_id)
);

CREATE TABLE watch_list (
  watch_list_id INT AUTO_INCREMENT PRIMARY KEY,
  mov_show_id INT NOT NULL,
  FOREIGN KEY (mov_show_id) REFERENCES movies_shows(mov_show_id)
)

ALTER TABLE users
ADD COLUMN validationcode VARCHAR(6) AFTER hashed_password;

ALTER TABLE users
ADD COLUMN isvalidation TINYINT(1) AFTER validationcode;
