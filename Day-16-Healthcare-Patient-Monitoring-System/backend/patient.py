class Patient:
    def __init__(self,
                 patient_id,
                 age,
                 gender,
                 diagnosis,
                 admission_type,
                 comorbidity_count):
        self.patient_id = patient_id
        self.age = age
        self.gender = gender
        self.diagnosis  = diagnosis
        self.admission_type = admission_type
        self.comorbidity_count = comorbidity_count

    def get_patient_info(self):
        return{
            "patient_id": self.patient_id,
            "age": self.age,
            "gender": self.gender,
            "diagnosis": self.diagnosis,
            "admission_type": self.admission_type,
            "comorbidity_count": self.comorbidity_count
        }