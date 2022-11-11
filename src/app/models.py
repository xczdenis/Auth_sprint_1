import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.decorators import trace
from app.hashers import check_password, make_password

users_permissions_association = db.Table(
    "users_permissions",
    db.metadata,
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id")),
    db.Column("permission_id", UUID(as_uuid=True), db.ForeignKey("permissions.id")),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    login = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    entry_records = db.relationship("EntryRecord", back_populates="user", cascade="all,delete")
    social_accounts = db.relationship("SocialAccount", back_populates="user", cascade="all,delete")
    permissions = db.relationship(
        "Permission",
        secondary=users_permissions_association,
        back_populates="users",
        cascade="all, delete",
    )

    def __repr__(self):
        return f"<User {self.login}>"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def log_entry(self, **kwargs):
        log = EntryRecord()
        log.user = self
        log.user_agent = kwargs.get("User-Agent")
        db.session.add(log)
        db.session.commit()

    def remove_entry(self, **kwargs):
        user_agent = kwargs.get("User-Agent")
        EntryRecord.query.filter_by(user=self, user_agent=user_agent).delete()
        db.session.commit()

    @staticmethod
    @trace()
    def get_or_create(**kwargs):
        login = kwargs.get("login")
        email = kwargs.get("email")
        password = kwargs.get("password")

        user_query = User.query.filter_by(email=email)
        if login and not email:
            user_query = User.query.filter_by(login=login)
        user = user_query.first()

        if not user:
            user = User()
            user.login = login
            user.email = email
            user.set_password(password or "123")

            db.session.add(user)
            db.session.commit()

        return user

    def to_dict(self):
        return {
            "id": self.id,
            "login": self.login,
            "is_superuser": self.is_superuser,
            "permissions": [item.to_dict() for item in self.permissions],
        }


class EntryRecord(db.Model):
    __tablename__ = "entry_records"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    user_agent = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"))
    user = db.relationship("User", back_populates="entry_records")

    def to_dict(self):
        return {"user_agent": self.user_agent, "created": self.created}


class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    codename = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship(
        "User",
        secondary=users_permissions_association,
        back_populates="permissions",
    )

    def to_dict(self):
        return {"id": self.id, "codename": self.codename, "name": self.name}


class SocialAccount(db.Model):
    __tablename__ = "social_accounts"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    provider = db.Column(db.String, nullable=False)
    social_id = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    login = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"))
    user = db.relationship("User", back_populates="social_accounts")

    @staticmethod
    @trace()
    def get_or_create(provider: str, social_id: str, update: bool = True, **kwargs):
        email = kwargs.get("email")
        login = kwargs.get("login")
        user = kwargs.get("user")

        def update_attr(obj, attr, value):
            if value:
                setattr(obj, attr, value)

        social_account = (
            db.session.query(SocialAccount)
            .filter(SocialAccount.provider == provider, SocialAccount.social_id == social_id)
            .first()
        )

        if not social_account:
            social_account = SocialAccount()
            update = True

        if update:
            update_attr(social_account, "provider", provider)
            update_attr(social_account, "social_id", social_id)
            update_attr(social_account, "email", email)
            update_attr(social_account, "login", login)
            update_attr(social_account, "user", user)

            db.session.add(social_account)
            db.session.commit()

        return social_account

    def to_dict(self):
        return {
            "id": self.id,
            "provider": self.provider,
            "social_id": self.social_id,
            "login": self.login,
            "email": self.email,
            "user": self.user.to_dict(),
        }
