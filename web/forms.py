from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[
        FileRequired(),
        FileAllowed(['txt', 'pdf', 'docx'], 'Only text, PDF, image files are allowed!')
    ])
    submit = SubmitField('Upload')

class QuestionForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    num_mcqs = IntegerField('Number of MCQs', validators=[DataRequired()])
    num_short_desc = IntegerField('Number of Short Description Questions', validators=[DataRequired()])
    num_long_desc = IntegerField('Number of Long Description Questions', validators=[DataRequired()])
    num_case_studies = IntegerField('Number of Case Studies', validators=[DataRequired()])
    submit = SubmitField('Generate Questions')

class EvaluateForm(FlaskForm):
    student_answer = TextAreaField('Student Answer', validators=[DataRequired()])
    expert_answer = TextAreaField('Expert Answer', validators=[DataRequired()])
    submit = SubmitField('Evaluate Answer')

class AnswerForm(FlaskForm):
    mcq_answers = TextAreaField('MCQ Answers', validators=[DataRequired()])
    short_desc_answers = TextAreaField('Short Description Answers', validators=[DataRequired()])
    long_desc_answers = TextAreaField('Long Description Answers', validators=[DataRequired()])
    case_studies_answers = TextAreaField('Case Studies Answers', validators=[DataRequired()])
    submit = SubmitField('Submit Answers')