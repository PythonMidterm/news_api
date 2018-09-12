from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy.fields import fields
from . import Feed, Account, AccountRole, Preferences


class AccountRoleSchema(ModelSchema):
    class Meta:
        model = AccountRole


class AccountSchema(ModelSchema):
    roles = fields.Nested(AccountRoleSchema, many=True, only='name')

    class Meta:
        model = Account


class PreferencesSchema(ModelSchema):
    class Meta:
        model = Preferences


class FeedSchema(ModelSchema):
    class Meta:
        model = Feed
