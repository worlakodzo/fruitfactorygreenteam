 
CREATE DATABASE IF NOT EXISTS weight; 
USE weight;

CREATE TABLE `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;
 
CREATE TABLE `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

show tables;

describe containers_registered;
describe transactions;
 
insert into `containers_registered`(`container_id`,`weight`,`unit`) values
('C-35434', '296', 'kg'),
('C-73281', '273', 'kg'),
('C-35537', '292', 'kg'),
('C-49036', '272', 'kg'),
('C-85957', '274', 'kg'),
('C-57132', '306', 'kg'),
('C-80015', '285', 'kg'),
('C-40162', '255', 'kg'),
('C-66667', '238', 'kg'),
('C-65481', '306', 'kg'),
('C-65816', '270', 'kg'),
('C-38068', '267', 'kg'),
('C-36882', '286', 'kg'),
('C-38559', '253', 'kg'),
('C-83754', '247', 'kg'),
('C-40277', '307', 'kg'),
('C-55516', '260', 'kg'),
('C-45237', '301', 'kg'),
('C-69828', '269', 'kg'),
('C-44997', '250', 'kg'),
('C-52273', '308', 'kg'),
('C-63478', '245', 'kg'),
('C-42418', '286', 'kg'),
('C-86865', '299', 'kg'),
('C-38552', '266', 'kg'),
('C-81185', '242', 'kg'),
('C-71151', '300', 'kg'),
('C-78131', '273', 'kg'),
('C-61969', '289', 'kg'),
('C-82193', '308', 'kg'),
('C-85358', '259', 'kg'),
('C-47634', '285', 'kg'),
('C-83570', '278', 'kg'),
('C-45628', '288', 'kg'),
('C-70986', '251', 'kg'),
('C-54804', '297', 'kg'),
('K-8263', '666', 'lbs'),
('K-5269', '666', 'lbs'),
('K-7943', '644', 'lbs'),
('K-5355', '642', 'lbs'),
('K-8120', '657', 'lbs'),
('K-4987', '653', 'lbs'),
('K-5867', '666', 'lbs'),
('K-3963', '541', 'lbs'),
('K-8298', '554', 'lbs'),
('K-4722', '530', 'lbs'),
('K-7947', '589', 'lbs'),
('K-6176', '523', 'lbs'),
('K-3690', '682', 'lbs'),
('K-7488', '633', 'lbs'),
('K-8128', '528', 'lbs'),
('K-4743', '572', 'lbs'),
('K-6350', '550', 'lbs'),
('K-7425', '677', 'lbs'),
('K-7714', '525', 'lbs'),
('K-4109', '587', 'lbs'),
('K-5768', '569', 'lbs');

insert into `transactions`(`id`,`datetime`,`direction`,`truck`,`containers`,`bruto`,`truckTara`,`neto`,`produce`) values
(10001,'2022-01-01 12:24:56','in','t0001','K-7714',1000,500,500,'oranges'),
(10002,'2022-01-01 12:26:56','out','t0001','K-7714',1000,500,500,'oranges'),
(10003,'2022-01-01 12:27:56','in','s0001','K-5768',1000,500,500,'apples'),
(10004,'2022-01-01 12:28:56','out','s0001','K-5768',1000,500,500,'apples');

