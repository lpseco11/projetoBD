CREATE TABLE employe (
	employe_id	 VARCHAR(512),
	name		 VARCHAR(512),
	contact_info	 VARCHAR(512),
	password	 VARCHAR(512),
	contract_details VARCHAR(512),
	PRIMARY KEY(employe_id)
);

CREATE TABLE doctor (
	medical_license	 VARCHAR(512),
	specialization	 VARCHAR(512),
	employe_employe_id VARCHAR(512),
	PRIMARY KEY(employe_employe_id)
);

CREATE TABLE nurse (
	internal_hierarchical_category VARCHAR(512),
	employe_employe_id		 VARCHAR(512),
	PRIMARY KEY(employe_employe_id)
);

CREATE TABLE assistant (
	employe_employe_id VARCHAR(512),
	PRIMARY KEY(employe_employe_id)
);

CREATE TABLE patient (
	patient_id	 VARCHAR(512),
	name	 VARCHAR(512),
	contact_info VARCHAR(512),
	password	 VARCHAR(512),
	PRIMARY KEY(patient_id)
);

CREATE TABLE appointments (
	appointment_id		 VARCHAR(512),
	appointment_datetime	 TIMESTAMP,
	patient_patient_id		 VARCHAR(512) NOT NULL,
	assistant_employe_employe_id VARCHAR(512) NOT NULL,
	doctor_employe_employe_id	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(appointment_id)
);

CREATE TABLE hospitalization (
	hospitalization_id		 VARCHAR(512),
	patient_patient_id		 VARCHAR(512) NOT NULL,
	assistant_employe_employe_id VARCHAR(512) NOT NULL,
	nurse_employe_employe_id	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(hospitalization_id)
);

CREATE TABLE surgery (
	surgery_id			 VARCHAR(512),
	doctor_employe_employe_id		 VARCHAR(512) NOT NULL,
	hospitalization_hospitalization_id VARCHAR(512) NOT NULL,
	PRIMARY KEY(surgery_id)
);

CREATE TABLE prescription (
	prescription_id			 VARCHAR(512),
	hospitalization_hospitalization_id VARCHAR(512) NOT NULL,
	appointments_appointment_id	 VARCHAR(512) NOT NULL,
	PRIMARY KEY(prescription_id)
);

CREATE TABLE medication (
	medication_id		 VARCHAR(512),
	name			 VARCHAR(512),
	dosage			 NUMERIC(8,2),
	prescription_prescription_id VARCHAR(512),
	PRIMARY KEY(medication_id,prescription_prescription_id)
);

CREATE TABLE side_effects (
	side_effect_id				 VARCHAR(512),
	name					 VARCHAR(512),
	probability				 VARCHAR(512),
	severity				 VARCHAR(512),
	medication_medication_id		 VARCHAR(512),
	medication_prescription_prescription_id VARCHAR(512),
	PRIMARY KEY(side_effect_id,medication_medication_id,medication_prescription_prescription_id)
);

CREATE TABLE bill (
	bill_id				 VARCHAR(512),
	cost				 NUMERIC(8,2),
	hospitalization_hospitalization_id VARCHAR(512),
	appointments_appointment_id	 VARCHAR(512),
	PRIMARY KEY(bill_id)
);

CREATE TABLE nurse_surgery (
	nurse_employe_employe_id VARCHAR(512),
	surgery_surgery_id	 VARCHAR(512),
	PRIMARY KEY(nurse_employe_employe_id,surgery_surgery_id)
);

CREATE TABLE nurse_appointments (
	nurse_employe_employe_id	 VARCHAR(512),
	appointments_appointment_id VARCHAR(512),
	PRIMARY KEY(nurse_employe_employe_id,appointments_appointment_id)
);

ALTER TABLE doctor ADD CONSTRAINT doctor_fk1 FOREIGN KEY (employe_employe_id) REFERENCES employe(employe_id);
ALTER TABLE nurse ADD CONSTRAINT nurse_fk1 FOREIGN KEY (employe_employe_id) REFERENCES employe(employe_id);
ALTER TABLE assistant ADD CONSTRAINT assistant_fk1 FOREIGN KEY (employe_employe_id) REFERENCES employe(employe_id);
ALTER TABLE appointments ADD CONSTRAINT appointments_fk1 FOREIGN KEY (patient_patient_id) REFERENCES patient(patient_id);
ALTER TABLE appointments ADD CONSTRAINT appointments_fk2 FOREIGN KEY (assistant_employe_employe_id) REFERENCES assistant(employe_employe_id);
ALTER TABLE appointments ADD CONSTRAINT appointments_fk3 FOREIGN KEY (doctor_employe_employe_id) REFERENCES doctor(employe_employe_id);
ALTER TABLE hospitalization ADD CONSTRAINT hospitalization_fk1 FOREIGN KEY (patient_patient_id) REFERENCES patient(patient_id);
ALTER TABLE hospitalization ADD CONSTRAINT hospitalization_fk2 FOREIGN KEY (assistant_employe_employe_id) REFERENCES assistant(employe_employe_id);
ALTER TABLE hospitalization ADD CONSTRAINT hospitalization_fk3 FOREIGN KEY (nurse_employe_employe_id) REFERENCES nurse(employe_employe_id);
ALTER TABLE surgery ADD CONSTRAINT surgery_fk1 FOREIGN KEY (doctor_employe_employe_id) REFERENCES doctor(employe_employe_id);
ALTER TABLE surgery ADD CONSTRAINT surgery_fk2 FOREIGN KEY (hospitalization_hospitalization_id) REFERENCES hospitalization(hospitalization_id);
ALTER TABLE prescription ADD CONSTRAINT prescription_fk1 FOREIGN KEY (hospitalization_hospitalization_id) REFERENCES hospitalization(hospitalization_id);
ALTER TABLE prescription ADD CONSTRAINT prescription_fk2 FOREIGN KEY (appointments_appointment_id) REFERENCES appointments(appointment_id);
ALTER TABLE medication ADD CONSTRAINT medication_fk1 FOREIGN KEY (prescription_prescription_id) REFERENCES prescription(prescription_id);
ALTER TABLE side_effects ADD CONSTRAINT side_effects_fk1 FOREIGN KEY (medication_medication_id, medication_prescription_prescription_id) REFERENCES medication(medication_id, prescription_prescription_id);
ALTER TABLE bill ADD CONSTRAINT bill_fk1 FOREIGN KEY (hospitalization_hospitalization_id) REFERENCES hospitalization(hospitalization_id);
ALTER TABLE bill ADD CONSTRAINT bill_fk2 FOREIGN KEY (appointments_appointment_id) REFERENCES appointments(appointment_id);
ALTER TABLE nurse_surgery ADD CONSTRAINT nurse_surgery_fk1 FOREIGN KEY (nurse_employe_employe_id) REFERENCES nurse(employe_employe_id);
ALTER TABLE nurse_surgery ADD CONSTRAINT nurse_surgery_fk2 FOREIGN KEY (surgery_surgery_id) REFERENCES surgery(surgery_id);
ALTER TABLE nurse_appointments ADD CONSTRAINT nurse_appointments_fk1 FOREIGN KEY (nurse_employe_employe_id) REFERENCES nurse(employe_employe_id);
ALTER TABLE nurse_appointments ADD CONSTRAINT nurse_appointments_fk2 FOREIGN KEY (appointments_appointment_id) REFERENCES appointments(appointment_id);

