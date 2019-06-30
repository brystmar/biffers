from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField


class BifSelector(FlaskForm):
    name = 'Select BIF'
    selector = SelectField('Select BIF', id='select_bif')

    def __repr__(self):  # tells python how to print objects of this class to the console while debugging
        return f'<BifSelector Name: {self.Meta.__name__}, Choices: {self.selector.choices}>'


class ScrapeNewThread(FlaskForm):
    name = 'Scrape New Thread'
    thread_name = StringField('Thread Name', id='new_thread_name', render_kw={'autofocus': True})
    url = StringField('URL', id='new_thread_url')

    submit = SubmitField(name, id='btn_scrape_new_thread', render_kw={'class': 'btn btn-success'})

    def __repr__(self):
        return f'<{self.name} form for {self.thread_name}>'


class ScrapeExistingThread(FlaskForm):
    name = 'Scrape Existing Thread'
    scrape = SubmitField(name, id='btn_scrape_existing_thread', render_kw={'class': 'btn btn-primary'})

    def __repr__(self):
        return f'<{self.name} Button>'


class UpdateLikes(FlaskForm):
    name = 'Update Likes'
    update_likes = SubmitField(name, id='btn_update_likes', render_kw={'class': 'btn btn-warning'})

    def __repr__(self):
        return f'<{self.name} Button>'


class CustomOutput(FlaskForm):
    name = 'Custom Output'
    custom_output = SubmitField(name, id='btn_custom_output', render_kw={'class': 'btn btn-info'})

    def __repr__(self):
        return f'<{self.name} Button>'

# choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')]
