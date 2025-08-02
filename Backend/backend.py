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
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    medical_history = db.Column(db.Text, nullable=False)
    medications = db.Column(db.Text, nullable=False)
    allergies = db.Column(db.Text, nullable=False)
    emergency_contact = db.Column(db.String(100), nullable=False)

@app.route('/<email>/<password>', methods=['GET'])
def login(email, password):
    patient = Patient.query.filter_by(email=email, password=password).first()
    if patient:
        return jsonify({'id': patient.id}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return jsonify({
        'name': patient.name,
        'medical_history': patient.medical_history,
        'medications': patient.medications,
        'allergies': patient.allergies,
        'emergency_contact': patient.emergency_contact
    })

def seed_database():
    if not os.path.exists('patients.db'):
        with app.app_context():
            db.create_all()
            sample_patients = [
                Patient(name="Alice Johnson", email="alice.johnson@example.com", password="Password123", medical_history="Asthma", medications="Ventolin", allergies="Pollen", emergency_contact="Bob Johnson: 555-1234"),
                Patient(name="Ben Smith", email="ben.smith@example.com", password="Password123", medical_history="Diabetes", medications="Insulin", allergies="None", emergency_contact="Sally Smith: 555-2345"),
                Patient(name="Carol Lee", email="carol.lee@example.com", password="Password123", medical_history="Hypertension", medications="Amlodipine", allergies="Penicillin", emergency_contact="Tim Lee: 555-3456"),
                Patient(name="David Kim", email="david.kim@example.com", password="Password123", medical_history="None", medications="None", allergies="Peanuts", emergency_contact="Susan Kim: 555-4567"),
                Patient(name="Emily Tran", email="emily.tran@example.com", password="Password123", medical_history="Epilepsy", medications="Lamotrigine", allergies="None", emergency_contact="John Tran: 555-5678"),
                Patient(name="Frank White", email="frank.white@example.com", password="Password123", medical_history="High cholesterol", medications="Atorvastatin", allergies="Shellfish", emergency_contact="Linda White: 555-6789"),
                Patient(name="Grace Park", email="grace.park@example.com", password="Password123", medical_history="Thyroid disorder", medications="Levothyroxine", allergies="Latex", emergency_contact="George Park: 555-7890"),
                Patient(name="Hannah Zhao", email="hannah.zhao@example.com", password="Password123", medical_history="Migraine", medications="Sumatriptan", allergies="None", emergency_contact="Kevin Zhao: 555-8901"),
                Patient(name="Ian Brown", email="ian.brown@example.com", password="Password123", medical_history="Arthritis", medications="Ibuprofen", allergies="Cats", emergency_contact="Laura Brown: 555-9012"),
                Patient(name="Jackie Wilson", email="jackie.wilson@example.com", password="Password123", medical_history="Cancer survivor", medications="Tamoxifen", allergies="Gluten", emergency_contact="Mark Wilson: 555-0123"),
                Patient(name="Karen Davis", email="karen.davis@example.com", password="Password123", medical_history="Heart disease", medications="Metoprolol", allergies="Soy", emergency_contact="Daniel Davis: 555-1122"),
                Patient(name="Leo Scott", email="leo.scott@example.com", password="Password123", medical_history="Depression", medications="Sertraline", allergies="Bees", emergency_contact="Mia Scott: 555-2233"),
                Patient(name="Maria Gonzalez", email="maria.gonzalez@example.com", password="Password123", medical_history="Pregnancy", medications="Prenatal vitamins", allergies="Nuts", emergency_contact="Carlos Gonzalez: 555-3344"),
                Patient(name="Nathan Young", email="nathan.young@example.com", password="Password123", medical_history="GERD", medications="Omeprazole", allergies="Dust", emergency_contact="Nina Young: 555-4455"),
                Patient(name="Olivia Reed", email="olivia.reed@example.com", password="Password123", medical_history="Kidney stones", medications="Hydrochlorothiazide", allergies="Dairy", emergency_contact="Peter Reed: 555-5566"),
            ]
            db.session.bulk_save_objects(sample_patients)
            db.session.commit()

if __name__ == '__main__':
    seed_database()
    app.run(debug=True)
