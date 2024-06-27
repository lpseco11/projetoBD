
INSERT INTO employe (employe_id, name, contact_info, password, contract_details)
VALUES ('12', 'John Doe', 'john@gmail.com', 'password123', 'Full-time');


INSERT INTO employe (employe_id, name, contact_info, password, contract_details)
VALUES ('13', 'Emily Brown', 'emily@gmail.com', 'nursepass', 'Part-time');


INSERT INTO employe (employe_id, name, contact_info, password, contract_details)
VALUES ('14', 'Michael Johnson', 'michael@gmail.com', 'assistantpass', 'Full-time');



INSERT INTO doctor (medical_license, specialization, employe_employe_id)
VALUES ('DOC123', 'Cardiology', '12');


INSERT INTO nurse (internal_hierarchical_category, employe_employe_id)
VALUES ('Senior', '13'); 

INSERT INTO assistant (employe_employe_id)
VALUES ('14'); 


INSERT INTO patient (patient_id, name, contact_info, password)
VALUES ('2', 'Alice Smith','alice@gmail.com', 'password456');


INSERT INTO appointments (appointment_id, appointment_datetime, patient_patient_id, assistant_employe_employe_id, doctor_employe_employe_id)
VALUES ('17', NOW(), '2', '14', '12'); 

INSERT INTO hospitalization (hospitalization_id, patient_patient_id, assistant_employe_employe_id, nurse_employe_employe_id, date)
VALUES ('19', '2', '14', '13', '2024-06-12'); 


INSERT INTO surgery (surgery_id, doctor_employe_employe_id, hospitalization_hospitalization_id)
VALUES ('15', '12', '19'); 
