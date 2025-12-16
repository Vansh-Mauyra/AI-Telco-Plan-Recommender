-- =============================
-- SAMPLE DATA INSERTS
-- =============================

-- 1. Carriers
INSERT INTO carrier (carrier_name, description, website) VALUES
('Airtel', 'Bharti Airtel telecom services', 'https://www.airtel.in'),
('Jio', 'Reliance Jio Infocomm', 'https://www.jio.com'),
('Vi', 'Vodafone Idea Limited', 'https://www.myvi.in');


-- 2. Telco Plans
INSERT INTO telco_plan
(carrier_id, plan_name, plan_code, monthly_fee, validity_days, plan_type,
 data_gb, daily_data_gb, voice_minutes, sms_count, network_type)
VALUES
-- Airtel
(1,'Airtel 199','AT199',199,28,'prepaid',25,1,1000,100,'4G'),
(1,'Airtel  249','AT249',249,28,'prepaid',40,1.5,2000,100,'4G'),

-- Jio
(2,'Jio 209','J209',209,28,'prepaid',30,1,1500,100,'4G'),
(2,'Jio 259','J259',259,28,'prepaid',50,1.5,2000,100,'4G'),

-- Vi
(3,'Vi 199','VI199',199,28,'prepaid',24,1,1000,100,'4G'),
(3,'Vi 299','VI299',299,28,'prepaid',48,1.5,2000,100,'4G');
INSERT INTO telco_plan (
    carrier_id, plan_name, plan_code, monthly_fee, validity_days, plan_type,
    data_gb, daily_data_gb, voice_minutes, sms_count,
    roaming_included, international_roaming, network_type,
    contract_months, is_active, created_at, updated_at
) VALUES
-- Airtel
(1,'Airtel 499','AT499',499,28,'prepaid',90,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),
(1,'Airtel 699','AT699',699,56,'prepaid',150,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),

-- Jio
(2,'Jio 449','J449',449,28,'prepaid',84,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),
(2,'Jio 666','J666',666,56,'prepaid',168,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),

-- Vi
(3,'Vi 459','VI459',459,28,'prepaid',84,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),
(3,'Vi 701','VI701',701,56,'prepaid',168,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW());
INSERT INTO telco_plan (
    carrier_id, plan_name, plan_code, monthly_fee, validity_days, plan_type,
    data_gb, daily_data_gb, voice_minutes, sms_count,
    roaming_included, international_roaming, network_type,
    contract_months, is_active, created_at, updated_at
) VALUES
-- Airtel
(1,'Airtel Unlimited 5G 999','AT999',999,84,'prepaid',240,3,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),
(1,'Airtel Unlimited 5G 1199','AT1199',1199,84,'prepaid',300,3,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),

-- Jio
(2,'Jio True 5G 899','J899',899,84,'prepaid',240,3,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),
(2,'Jio True 5G 1099','J1099',1099,84,'prepaid',300,3,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),

-- Vi
(3,'Vi Unlimited 5G 901','VI901',901,84,'prepaid',240,3,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),
(3,'Vi Unlimited 5G 1201','VI1201',1201,84,'prepaid',300,3,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW());
INSERT INTO telco_plan (
    carrier_id, plan_name, plan_code, monthly_fee, validity_days, plan_type,
    data_gb, daily_data_gb, voice_minutes, sms_count,
    roaming_included, international_roaming, network_type,
    contract_months, is_active, created_at, updated_at
) VALUES
(1,'Airtel Annual 2999','AT2999',2999,365,'prepaid',720,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),
(2,'Jio Annual 2879','J2879',2879,365,'prepaid',730,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW()),
(3,'Vi Annual 2899','VI2899',2899,365,'prepaid',720,2,3000,100,FALSE,FALSE,'5G',0,TRUE,NOW(),NOW());
INSERT INTO telco_plan (
    carrier_id, plan_name, plan_code, monthly_fee, validity_days, plan_type,
    data_gb, daily_data_gb, voice_minutes, sms_count,
    roaming_included, international_roaming, network_type,
    contract_months, is_active, created_at, updated_at
) VALUES
(1,'Airtel IR 799','ATIR799',799,30,'prepaid',10,0,500,50,TRUE,TRUE,'4G',0,TRUE,NOW(),NOW()),
(2,'Jio IR 1101','JIR1101',1101,30,'prepaid',15,0,500,50,TRUE,TRUE,'4G',0,TRUE,NOW(),NOW()),
(3,'Vi IR 899','VIIR899',899,30,'prepaid',12,0,500,50,TRUE,TRUE,'4G',0,TRUE,NOW(),NOW());



-- 3. Addons
INSERT INTO addon
(carrier_id, addon_name, price, data_gb, validity_days)
VALUES
(1,'Airtel Data Booster 10GB',98,10,28),
(1,'Airtel Data Booster 50GB',301,50,28),
(2,'Jio Data Booster 6GB',61,6,28),
(2,'Jio Data Booster 25GB',222,25,28),
(3,'Vi Data Booster 12GB',121,12,28),
(3,'Vi Data Booster 50GB',351,50,28);


-- 4. Customers
INSERT INTO customer_profile
(phone_number, email, name, current_carrier_id, current_plan_id,
 avg_monthly_data_gb, avg_voice_minutes, avg_sms, budget)
VALUES
-- Budget 
('9876543210','rahul@gmail.com','Rahul Sharma',1,1,18,400,40,299),
-- Student
('9876543211','neha@gmail.com','Neha Verma',2,3,45,800,60,399),
-- Professional
('9876543212','arjun@gmail.com','Arjun Mehta',1,5,120,1500,100,699),
-- Power User
('9876543213','rohit@gmail.com','Rohit Iyer',2,8,220,2500,100,999),
-- International Traveler
('9876543214','priya@gmail.com','Priya Nair',1,15,35,600,50,899),
-- Voice Heavy
('9876543215','amit@gmail.com','Amit Singh',3,6,25,3000,200,459),
-- Corporate User
('9876543216','sneha@gmail.com','Sneha Kapoor',2,9,180,2000,100,1099),
-- Senior Citizen
('9876543217','ramesh@gmail.com','Ramesh Rao',3,2,12,2500,150,299);


-- 5. Usage History
INSERT INTO usage_history
(customer_id, month, data_gb, voice_minutes, sms, roaming_charges, international_usage)
VALUES

-- -------------------------
-- Budget  (Low usage)
-- -------------------------
(1, '2025-01-01', 15.2, 380, 35, 0, FALSE),
(1, '2025-02-01', 17.8, 410, 40, 0, FALSE),
(1, '2025-03-01', 16.5, 395, 38, 0, FALSE),

-- -------------------------
-- Student (High data, low calls)
-- -------------------------
(2, '2025-01-01', 42.5, 750, 55, 0, FALSE),
(2, '2025-02-01', 47.8, 820, 60, 0, FALSE),
(2, '2025-03-01', 44.1, 790, 58, 0, FALSE),

-- -------------------------
-- Professional (Balanced heavy)
-- -------------------------
(3, '2025-01-01', 115.6, 1400, 95, 0, FALSE),
(3, '2025-02-01', 122.3, 1550, 105, 0, FALSE),
(3, '2025-03-01', 118.9, 1480, 100, 0, FALSE),

-- -------------------------
-- Power User (Extreme everything)
-- -------------------------
(4, '2025-01-01', 210.4, 2400, 95, 0, FALSE),
(4, '2025-02-01', 225.9, 2600, 110, 0, FALSE),
(4, '2025-03-01', 218.7, 2550, 100, 0, FALSE),

-- -------------------------
-- International Traveler
-- -------------------------
(5, '2025-01-01', 30.5, 550, 45, 850.00, TRUE),
(5, '2025-02-01', 34.2, 620, 50, 1200.00, TRUE),
(5, '2025-03-01', 36.8, 580, 48, 980.00, TRUE),

-- -------------------------
-- Voice Heavy (Calls > Data)
-- -------------------------
(6, '2025-01-01', 22.1, 2900, 180, 0, FALSE),
(6, '2025-02-01', 24.3, 3100, 210, 0, FALSE),
(6, '2025-03-01', 23.7, 3050, 200, 0, FALSE),

-- -------------------------
-- Corporate User (Premium usage)
-- -------------------------
(7, '2025-01-01', 165.8, 1900, 95, 300.00, TRUE),
(7, '2025-02-01', 178.4, 2100, 110, 450.00, TRUE),
(7, '2025-03-01', 185.2, 2050, 105, 400.00, TRUE),

-- -------------------------
-- Senior Citizen (Low data, high calls)
-- -------------------------
(8, '2025-01-01', 10.8, 2400, 140, 0, FALSE),
(8, '2025-02-01', 11.5, 2550, 150, 0, FALSE),
(8, '2025-03-01', 12.2, 2600, 155, 0, FALSE);
