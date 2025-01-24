import os
import json
import hashlib
from datetime import datetime, timedelta
import uuid
from funciones import resource_path, get_user_data_path

ACTIVATION_FILE = get_user_data_path("activation.json")
SECRET_KEY = "Y2h3bG9uZ2VyU2VjcmV0S2V5Q2hhbmdlVGhpcyE="  # Reemplaza esto con una clave secreta segura generada

def load_activation_data():
    if os.path.exists(ACTIVATION_FILE):
        with open(ACTIVATION_FILE, "r") as file:
            return json.load(file)
    return {}

def save_activation_data(data):
    with open(ACTIVATION_FILE, "w") as file:
        json.dump(data, file)

def generate_business_id():
    return hashlib.sha256(uuid.uuid4().bytes).hexdigest()[:8]

def generate_validation_code(date_str, business_id):
    data = date_str + business_id + SECRET_KEY
    return hashlib.sha256(data.encode()).hexdigest()[:10]  # Generar un hash y tomar los primeros 10 caracteres

def check_activation():
    data = load_activation_data()
    if "activation_date" in data and "validation_code" in data:
        if data.get("no_monthly_validation", False):
            return True, None
        activation_date = datetime.strptime(data["activation_date"], "%Y-%m-%d")
        validation_code = data["validation_code"]
        if datetime.now() > activation_date + timedelta(days=30):
            return False, validation_code
        if not data.get("validated", False):
            return False, validation_code
        return True, None
    else:
        activation_date = datetime.now().strftime("%Y-%m-%d")
        business_id = generate_business_id()
        validation_code = generate_validation_code(activation_date, business_id)
        save_activation_data({"activation_date": activation_date, "validation_code": validation_code, "validated": False, "business_id": business_id})
        return False, validation_code

def validate_code(input_code, business_id):
    data = load_activation_data()
    if data:
        expected_code = generate_validation_code(data["activation_date"], business_id)
        if input_code == expected_code:
            new_activation_date = datetime.now().strftime("%Y-%m-%d")
            new_validation_code = generate_validation_code(new_activation_date, business_id)
            save_activation_data({"activation_date": new_activation_date, "validation_code": new_validation_code, "validated": True, "business_id": business_id})
            return True
        elif input_code == "delunoalocho":  # Reemplaza "SPECIAL_CODE" con el código especial que desactiva la validación mensual
            save_activation_data({"activation_date": data["activation_date"], "validation_code": data["validation_code"], "validated": True, "business_id": business_id, "no_monthly_validation": True})
            return -1
    return False

def is_validated():
    data = load_activation_data()
    return data and data.get("validated", False)