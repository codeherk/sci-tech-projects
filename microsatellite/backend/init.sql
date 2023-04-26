CREATE DATABASE IF NOT EXISTS biology;

USE biology;

CREATE TABLE IF NOT EXISTS microsatellites (
  id INT(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  base VARCHAR(10) NOT NULL,
  repeats INT(11) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO microsatellites (name, base, repeats) VALUES 
('Thomas Jenkins', 'CA', 2),
('Maeve Chen', 'TTG', 3),
('Anjali Gupta', 'GCT', 4),
('Ricardo Santos', 'ATC', 5),
('Jessica Kim', 'GAA', 2);
