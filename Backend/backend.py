from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Demographics
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    marital_status = db.Column(db.String(20), nullable=True)
    ethnicity = db.Column(db.String(50), nullable=True)
    language = db.Column(db.String(50), nullable=True)
    
    # Authentication
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # Medical Information
    blood_type = db.Column(db.String(3), nullable=False)  # e.g., "O+", "AB-"
    medical_history = db.Column(db.Text, nullable=False)
    medications = db.Column(db.Text, nullable=False)
    allergies = db.Column(db.Text, nullable=False)
    immunizations = db.Column(db.Text, nullable=True)
    past_surgeries = db.Column(db.Text, nullable=True)
    chronic_conditions = db.Column(db.Text, nullable=True)
    family_medical_history = db.Column(db.Text, nullable=True)
    smoking_status = db.Column(db.String(20), nullable=True)  # "Never", "Former", "Current"
    alcohol_use = db.Column(db.String(20), nullable=True)     # "None", "Occasional", "Regular"
    height_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)

    # Emergency and Provider Info
    emergency_contact = db.Column(db.String(100), nullable=False)
    primary_physician = db.Column(db.String(100), nullable=True)
    insurance_provider = db.Column(db.String(100), nullable=True)
    insurance_policy_number = db.Column(db.String(50), nullable=True)

    # Appointments
    last_visit_date = db.Column(db.Date, nullable=True)
    next_appointment_date = db.Column(db.Date, nullable=True)

    # Notes
    notes = db.Column(db.Text, nullable=True)

@app.route('/<email>/<password>', methods=['GET'])
def login(email, password):
    patient = Patient.query.filter_by(email=email, password=password).first()
    if patient:
        return jsonify({'id': patient.id}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

from flask import jsonify, abort

@app.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    return jsonify({
        'id': patient.id,
        'name': patient.name,
        'gender': patient.gender,
        'date_of_birth': patient.date_of_birth,
        'phone_number': patient.phone_number,
        'address': patient.address,
        'marital_status': patient.marital_status,
        'ethnicity': patient.ethnicity,
        'language': patient.language,
        'email': patient.email,
        'blood_type': patient.blood_type,
        'medical_history': patient.medical_history,
        'medications': patient.medications,
        'allergies': patient.allergies,
        'emergency_contact': patient.emergency_contact
    })

def seed_database():
    db.session.query(Patient).delete()
    db.session.commit()
    if not os.path.exists('patients.db'):
        with app.app_context():
            db.create_all()
            sample_patients = [
                Patient(
                    name="Alice Johnson",
                    email="alice.johnson@example.com",
                    password="Password123",
                    medical_history="Diagnosed with moderate persistent asthma since childhood. Occasional exacerbations during allergy season.",
                    medications="Albuterol (Ventolin) inhaler, Fluticasone (daily corticosteroid)",
                    allergies="Pollen, Dust mites",
                    emergency_contact="Bob Johnson (father): 555-1234",
                    date_of_birth="1990-04-12",
                    gender="Female",
                    phone_number="555-1111",
                    address="123 Maple St, Springfield, IL",
                    marital_status="Single",
                    ethnicity="White",
                    language="English",
                    blood_type="O+"
                ),
                Patient(
                    name="Ben Smith",
                    email="ben.smith@example.com",
                    password="Password123",
                    medical_history="Type 1 Diabetes diagnosed at age 12. Requires daily insulin and routine blood sugar monitoring.",
                    medications="Insulin Glargine (Lantus), Insulin Aspart (Novolog)",
                    allergies="None",
                    emergency_contact="Sally Smith (sister): 555-2345",
                    date_of_birth="1987-09-03",
                    gender="Male",
                    phone_number="555-2222",
                    address="456 Oak Ave, Madison, WI",
                    marital_status="Married",
                    ethnicity="White",
                    language="English",
                    blood_type="A+"
                ),
                Patient(
                    name="Carol Lee",
                    email="carol.lee@example.com",
                    password="Password123",
                    medical_history="Hypertension diagnosed 5 years ago. Managed with lifestyle changes and medication.",
                    medications="Amlodipine 10mg daily, Lisinopril 20mg daily",
                    allergies="Penicillin",
                    emergency_contact="Tim Lee (spouse): 555-3456",
                    date_of_birth="1975-11-23",
                    gender="Female",
                    phone_number="555-3333",
                    address="789 Pine Rd, Seattle, WA",
                    marital_status="Married",
                    ethnicity="Asian",
                    language="English",
                    blood_type="B+"
                ),
                Patient(
                    name="David Kim",
                    email="david.kim@example.com",
                    password="Password123",
                    medical_history="No chronic conditions. Occasional seasonal allergies.",
                    medications="Loratadine as needed",
                    allergies="Peanuts (anaphylactic), Tree nuts",
                    emergency_contact="Susan Kim (mother): 555-4567",
                    date_of_birth="2000-02-18",
                    gender="Male",
                    phone_number="555-4444",
                    address="321 Cedar St, Irvine, CA",
                    marital_status="Single",
                    ethnicity="Asian",
                    language="Korean",
                    blood_type="AB+"
                ),
                Patient(
                    name="Emily Tran",
                    email="emily.tran@example.com",
                    password="Password123",
                    medical_history="Epilepsy diagnosed in teenage years. Seizures well-controlled on medication.",
                    medications="Lamotrigine 200mg twice daily",
                    allergies="None",
                    emergency_contact="John Tran (brother): 555-5678",
                    date_of_birth="1996-07-15",
                    gender="Female",
                    phone_number="555-5555",
                    address="987 Birch Blvd, Denver, CO",
                    marital_status="Single",
                    ethnicity="Asian",
                    language="English",
                    blood_type="O-"
                ),
                Patient(
                    name="Frank White",
                    email="frank.white@example.com",
                    password="Password123",
                    medical_history="Diagnosed with hyperlipidemia (high cholesterol).",
                    medications="Atorvastatin 40mg daily",
                    allergies="Shellfish",
                    emergency_contact="Linda White (wife): 555-6789",
                    date_of_birth="1969-05-30",
                    gender="Male",
                    phone_number="555-6666",
                    address="246 Willow Way, Boston, MA",
                    marital_status="Married",
                    ethnicity="White",
                    language="English",
                    blood_type="A-"
                ),
                Patient(
                    name="Grace Park",
                    email="grace.park@example.com",
                    password="Password123",
                    medical_history="Hashimoto’s thyroiditis diagnosed in her 30s. Regular monitoring of TSH levels.",
                    medications="Levothyroxine 100mcg daily",
                    allergies="Latex, Penicillin",
                    emergency_contact="George Park (husband): 555-7890",
                    date_of_birth="1982-03-27",
                    gender="Female",
                    phone_number="555-7777",
                    address="654 Elm Dr, San Jose, CA",
                    marital_status="Married",
                    ethnicity="Asian",
                    language="Korean",
                    blood_type="B-"
                ),
                Patient(
                    name="Hannah Zhao",
                    email="hannah.zhao@example.com",
                    password="Password123",
                    medical_history="Chronic migraines triggered by stress and weather changes.",
                    medications="Sumatriptan as needed, Propranolol for prevention",
                    allergies="None",
                    emergency_contact="Kevin Zhao (father): 555-8901",
                    date_of_birth="1998-12-01",
                    gender="Female",
                    phone_number="555-8888",
                    address="852 Cypress Ln, Atlanta, GA",
                    marital_status="Single",
                    ethnicity="Asian",
                    language="Mandarin",
                    blood_type="AB-"
                ),
                Patient(
                    name="Ian Brown",
                    email="ian.brown@example.com",
                    password="Password123",
                    medical_history="Osteoarthritis in both knees, worsens with physical activity.",
                    medications="Ibuprofen 600mg as needed, Glucosamine supplements",
                    allergies="Cats (respiratory)",
                    emergency_contact="Laura Brown (daughter): 555-9012",
                    date_of_birth="1958-08-10",
                    gender="Male",
                    phone_number="555-9999",
                    address="369 Redwood Ct, Portland, OR",
                    marital_status="Widowed",
                    ethnicity="Black",
                    language="English",
                    blood_type="O+"
                ),
                Patient(
                    name="Jackie Wilson",
                    email="jackie.wilson@example.com",
                    password="Password123",
                    medical_history="Breast cancer survivor (in remission 3 years). Under ongoing hormonal therapy.",
                    medications="Tamoxifen 20mg daily",
                    allergies="Gluten (causes GI distress)",
                    emergency_contact="Mark Wilson (husband): 555-0123",
                    date_of_birth="1972-10-05",
                    gender="Female",
                    phone_number="555-0101",
                    address="753 Fir St, Raleigh, NC",
                    marital_status="Married",
                    ethnicity="White",
                    language="English",
                    blood_type="A+"
                )
            ]
            db.session.bulk_save_objects(sample_patients)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_database()

    app.run(debug=True)