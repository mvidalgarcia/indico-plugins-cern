from __future__ import unicode_literals

from indico.core.db.sqlalchemy import db, PyIntEnum
from indico_cern_access.models.access_requests import CERNAccessRequestState
from sqlalchemy import Boolean
from sqlalchemy.ext.hybrid import hybrid_property


class CERNAccessRequestRegForm(db.Model):
    __tablename__ = 'access_request_regforms'
    __table_args__ = {'schema': 'plugin_cern_access'}

    form_id = db.Column(
        db.ForeignKey('event_registration.forms.id'),
        primary_key=True
    )
    request_state = db.Column(
        PyIntEnum(CERNAccessRequestState),
        nullable=False,
        default=CERNAccessRequestState.not_requested
    )
    allow_unpaid = db.Column(
        Boolean,
        nullable=False,
        default=False
    )

    registration_form = db.relationship(
        'RegistrationForm',
        uselist=False,
        lazy=False,
        backref=db.backref('cern_access_request', uselist=False))

    @hybrid_property
    def is_active(self):
        return self.request_state != CERNAccessRequestState.withdrawn

    @is_active.expression
    def is_active(self):
        return self.request_state != CERNAccessRequestState.withdrawn
