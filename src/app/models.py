import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from app import db
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
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    entry_records = db.relationship("EntryRecord", back_populates="user", cascade="all,delete")
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
