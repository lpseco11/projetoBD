CREATE OR REPLACE FUNCTION update_bill_surgery()
    RETURNS TRIGGER AS
$$
BEGIN
    -- Update the bill for the given hospitalization
    UPDATE bill
    SET cost = cost + 75
    WHERE hospitalization_hospitalization_id = NEW.hospitalization_hospitalization_id;

    IF NOT FOUND THEN
        -- If no rows were updated, insert a new bill
        INSERT INTO bill (bill_id, cost, hospitalization_hospitalization_id, appointments_appointment_id,status)
        VALUES (NEW.hospitalization_hospitalization_id, 75, NEW.hospitalization_hospitalization_id, NULL, 'unpaid');
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION update_bill_appointment()
    RETURNS TRIGGER AS
$$
BEGIN
    -- Update the bill for the given appointment
    UPDATE bill
    SET cost = cost + 50
    WHERE appointments_appointment_id = NEW.appointment_id;

    -- Check if the update affected any rows
    IF NOT FOUND THEN
        -- If no rows were updated, insert a new bill
        INSERT INTO bill (bill_id, cost, hospitalization_hospitalization_id, appointments_appointment_id,status,money_paid)
        VALUES (NEW.appointment_id, 50, NULL, NEW.appointment_id, 'unpaid',0.00);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_bill_appointment_trigger
    AFTER INSERT
    ON appointments
    FOR EACH ROW
EXECUTE FUNCTION update_bill_appointment();

CREATE TRIGGER update_bill_surgery_trigger
    AFTER INSERT OR UPDATE
    ON surgery
    FOR EACH ROW
EXECUTE FUNCTION update_bill_surgery();
