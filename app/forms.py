# Forms that are generated as html by jinja2
from wtforms import StringField, BooleanField, SubmitField, RadioField, widgets, Form, SelectMultipleField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


# RadioField('<label>', choices=[('<value>','<text in html>')], ((optional)) default='<value')


# small form just to get a button
class SubmitForm(FlaskForm):
    submit = SubmitField('Submit Button')


# form to select the version
class VersionSelectionForm(FlaskForm):
    select_version = RadioField('Label',
                                choices=[('8', 'Version:  8'),
                                         ('9', 'Version:  9'),
                                         ('10', 'Version: 10'),
                                         ('11', 'Version: 11')])
    submit = SubmitField('Select Version')


# search repository form
class SearchRepositoryForm(FlaskForm):
    repository = StringField('Repository:', default='')
    in_scope = RadioField('Filter repositories in scope:',
                          choices=[('True', 'True'),
                                   ('False', 'False'),
                                   ('both', 'both')],
                          default='both')
    bp = RadioField('Filter based on BP',
                    choices=[('BP00', 'BP00 - Master Data'),
                             ('BP01', 'BP01 - CRM-Verkoopbeheer'),
                             ('BP02', 'BP02 - Aankoopbeheer'),
                             ('BP03', 'BP03 - Productiebeheer'),
                             ('BP04', 'BP04 - Magazijnbeheer'),
                             ('BP05', 'BP05 - Projectenbeheer'),
                             ('BP06', 'BP06 - Boekhouding'),
                             ('BP07', 'BP07 - Personeelsbeheer'),
                             ('BP08', 'BP08 - Point Of Sale'),
                             ('BP09', 'BP09 - Marketing'),
                             ('BP10', 'BP10 - Website'),
                             ('BP11', 'BP11 - E-Commerce'),
                             ('BP12', 'BP12 - Rapporten & Doc\'s'),
                             ('IT Infrastructuur', 'IT Infrastructuur'),
                             ('unspecified', 'unspecified')],
                    default='unspecified')
    select_version = RadioField('Select version, does not affect search results.'
                                'Enables clicking on the repository name to see its modules.',
                                choices=[('8', 'Version:  8'),
                                         ('9', 'Version:  9'),
                                         ('10', 'Version: 10'),
                                         ('11', 'Version: 11')],
                                default=('8'))
    submit = SubmitField('Search Repository')


# search module form
class SearchModuleForm(FlaskForm):
    select_version = RadioField('Select Version',
                                choices=[('8', 'Version:  8'),
                                         ('9', 'Version:  9'),
                                         ('10', 'Version: 10'),
                                         ('11', 'Version: 11')],
                                validators=[DataRequired()],
                                default='8')
    module = StringField('Module:', default='')
    customers = StringField('Customer(s):', default='')
    verticals = StringField('Vertical(s):', default='')
    search_readme = BooleanField('Search in README', default=False)
    installable_bool = RadioField('Filter Installable Modules:',
                                  choices=[('True', 'Installable: True'),
                                           ('False', 'Installable: False'),
                                           ('both', 'All results')],
                                  default='both')
    submit = SubmitField('Search Module')


# rating and review form
class RatingReviewForm(FlaskForm):
    rating = RadioField('Rating:',
                        choices=[('No score', 'No score'),
                                 ('0', '0'),
                                 ('1', '1'),
                                 ('2', '2'),
                                 ('3', '3'),
                                 ('4', '4'),
                                 ('5', '5')])  # ,default='No score'
    review = StringField('Review')
    delete_reviews = BooleanField('Delete previous reviews', default=False)
    submit = SubmitField('Place review')


# edit repository form
class EditRepositoryForm(FlaskForm):
    bp = RadioField('BP: ',
                    choices=[('BP00', 'BP00 - Master Data'),
                             ('BP01', 'BP01 - CRM-Verkoopbeheer'),
                             ('BP02', 'BP02 - Aankoopbeheer'),
                             ('BP03', 'BP03 - Productiebeheer'),
                             ('BP04', 'BP04 - Magazijnbeheer'),
                             ('BP05', 'BP05 - Projectenbeheer'),
                             ('BP06', 'BP06 - Boekhouding'),
                             ('BP07', 'BP07 - Personeelsbeheer'),
                             ('BP08', 'BP08 - Point Of Sale'),
                             ('BP09', 'BP09 - Marketing'),
                             ('BP10', 'BP10 - Website'),
                             ('BP11', 'BP11 - E-Commerce'),
                             ('BP12', 'BP12 - Rapporten & Doc\'s'),
                             ('IT Infrastructuur', 'IT Infrastructuur'),
                             ('unspecified', 'unspecified')],
                    default='unchanged')
    in_scope = RadioField('In Scope:',
                          choices=[('True', 'Yes'),
                                   ('False', 'No'),
                                   ('unchanged', 'unchanged')],
                          default='unchanged')
    employee = StringField('Employee:', default='')
    submit = SubmitField('Save changes')


# edit module form
class EditModuleForm(FlaskForm):

    customer_str = StringField('Customer(s) to add:', default='')
    vertical_str = StringField('Vertical(s) to add:', default='')

    delete_customers = BooleanField('Delete customers for this module', default=False)
    delete_verticals = BooleanField('Delete verticals for this module', default=False)

    submit = SubmitField('Save changes')
