

class Course():
    def __init__(self, course_id, course_name, course_type, course_credit, prereqs, predicted_grade, prediction_prob):
        self.course_id = course_id
        self.course_name = course_name
        self.course_type = course_type
        self.course_credit = course_credit
        self.prereqs = prereqs
        self.predicted_grade = predicted_grade
        self.prediction_prob = prediction_prob

    def get_predictions(self, filter_details):
        for subject in filter_details:
            if len(subject) == 1:
                min_grade = filter_details.pop(filter_details.index(subject))
        
import pickle
model = pickle.load(open('flaskr/mjvoting_model', 'rb'))
print(model.get_params())


