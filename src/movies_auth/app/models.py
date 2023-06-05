import enum
import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr

from movies_auth.app import db
from movies_auth.app.common.decorators import trace
from movies_auth.app.common.serializer import Field, Serializer
from movies_auth.app.secure.hashers import check_password, make_password

users_permissions_association = db.Table(
    "users_permissions",
    db.metadata,
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id")),
    db.Column("permission_id", UUID(as_uuid=True), db.ForeignKey("permissions.id")),
)


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(Serializer, BaseModel):
    __tablename__ = "users"

    class Meta:
        serializable_fields = ("id", "login", "is_superuser", "permissions")

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    login = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
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
        log.user_id = self.id
        log.user_agent = kwargs.get("User-Agent")
        log.device_type = DeviceType.OTHER
        db.session.add(log)
        db.session.commit()

    def remove_entry(self, **kwargs):
        user_agent = kwargs.get("User-Agent")
        EntryRecord.query.filter_by(user_id=self.id, user_agent=user_agent).delete()
        db.session.commit()

    def save_in_db(self):
        db.session.add(self)
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


class DeviceType(enum.Enum):
    NOTEBOOK = "notebook"
    DESKTOP = "desktop"
    TABLET = "tablet"
    PHONE = "phone"
    TV = "tv"
    OTHER = "other"


class EntryRecordMixin(Serializer):
    class Meta:
        serializable_fields = (
            "user_agent",
            "created",
            Field(name="device_type", fn="serialize_device_type"),
        )

    def serialize_device_type(self):
        return self.device_type.name

    @declared_attr
    def user_id(self):
        return db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"))

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    device_type = db.Column(db.Enum(DeviceType), primary_key=True)
    user_agent = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow)


class EntryRecord(EntryRecordMixin, db.Model):
    __tablename__ = "entry_records"
    __table_args__ = ({"postgresql_partition_by": "LIST (device_type)"},)


class EntryRecordNotebook(EntryRecordMixin, db.Model):
    __tablename__ = f"entry_records_{DeviceType.NOTEBOOK.value}"


class EntryRecordDesktop(EntryRecordMixin, db.Model):
    __tablename__ = f"entry_records_{DeviceType.DESKTOP.value}"


class EntryRecordTablet(EntryRecordMixin, db.Model):
    __tablename__ = f"entry_records_{DeviceType.TABLET.value}"


class EntryRecordPhone(EntryRecordMixin, db.Model):
    __tablename__ = f"entry_records_{DeviceType.PHONE.value}"


class EntryRecordTv(EntryRecordMixin, db.Model):
    __tablename__ = f"entry_records_{DeviceType.TV.value}"


class EntryRecordOther(EntryRecordMixin, db.Model):
    __tablename__ = f"entry_records_{DeviceType.OTHER.value}"


class Permission(Serializer, db.Model):
    __tablename__ = "permissions"

    class Meta:
        serializable_fields = "__all__"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    codename = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship(
        "User",
        secondary=users_permissions_association,
        back_populates="permissions",
    )


class SocialAccount(Serializer, db.Model):
    __tablename__ = "social_accounts"

    class Meta:
        serializable_fields = ("id", "provider", "social_id", "email", "login", "created")

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
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
