# File with models to create the database out of
# See the docs on what to do when a column is renamed or deleted
from app import db


# repository model, has everything related to repositories
class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name
    repository = db.Column(db.String(64), index=True)
    description = db.Column(db.String(240), index=True)
    in_scope = db.Column(db.String(3), index=True)
    bp = db.Column(db.String(20), index=True)
    # employee with experience with this repository
    employee = db.Column(db.String(64), index=True)

    # not used, but might be informative
    # the number of modules per version, for this repository
    m_8 = db.Column(db.String(4))
    m_9 = db.Column(db.String(4))
    m_10 = db.Column(db.String(4))
    m_11 = db.Column(db.String(4))
    readme = db.Column(db.String(10000))

    modules = db.relationship('Module', backref='repo_name_fk', lazy='dynamic')

    def __repr__(self):
        return '<Repository: {}, {}, {}, {}, {}, {}>'.format(
            self.id, self.repository, self.description, self.in_scope, self.bp,
            self.employee)


# module model, has everything related to modules, ForeignKey to repository 'repo_name'
class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name
    addon = db.Column(db.String(240), index=True)
    # not used
    version = db.Column(db.String(20))
    # not used
    summary = db.Column(db.String(240), index=True)

    # m_url_tested = db.Column(db.String(240), index=True)

    # module exists in version:  True='X' / False='-'
    version_8 = db.Column(db.String(10), index=True)
    version_9 = db.Column(db.String(10), index=True)
    version_10 = db.Column(db.String(10), index=True)
    version_11 = db.Column(db.String(10), index=True)

    # installable in version_x:  'True' / 'False'
    installable_8 = db.Column(db.String(10), index=True)
    installable_9 = db.Column(db.String(10), index=True)
    installable_10 = db.Column(db.String(10), index=True)
    installable_11 = db.Column(db.String(10), index=True)

    # readme exists in version_x: True='readme' / False='-'
    readme_8 = db.Column(db.String(20), index=True)
    readme_9 = db.Column(db.String(20), index=True)
    readme_10 = db.Column(db.String(20), index=True)
    readme_11 = db.Column(db.String(20), index=True)

    # actual text of readme in version_x, converted from .rst to .txt
    readme_text_8 = db.Column(db.String(10000))
    readme_text_9 = db.Column(db.String(10000))
    readme_text_10 = db.Column(db.String(10000))
    readme_text_11 = db.Column(db.String(10000))

    # rating given by user, values range:  'No score'  '0'  ...  '5'
    rating_8 = db.Column(db.String(50), index=True)
    rating_9 = db.Column(db.String(50), index=True)
    rating_10 = db.Column(db.String(50), index=True)
    rating_11 = db.Column(db.String(50), index=True)

    # review=text inputted by user, multiple reviews seperated by '||'
    review_8 = db.Column(db.String(10000))
    review_9 = db.Column(db.String(10000))
    review_10 = db.Column(db.String(10000))
    review_11 = db.Column(db.String(10000))

    # foreign key to link a repository to module
    repo_name = db.Column(db.String, db.ForeignKey('repository.repository'))

    def __repr__(self):
        return '<Module: {}, {}, {}>'.format(
            self.id, self.addon, self.repo_name)
