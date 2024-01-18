from __future__ import annotations

from typing import Optional, List
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id) -> User|None:
    return db.session.get(User, int(id))

stream_schedule = db.Table(
        "stream_schedule",
        sa.Column("stream_id", sa.ForeignKey("stream.id"), primary_key=True),
        sa.Column("schedule_id", sa.ForeignKey("schedule.id"), primary_key=True),
    )

class Stream(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True)
    ip_address: so.Mapped[int] = so.mapped_column(unique=True)
    api: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    schedules: so.Mapped[List[Schedule]] = so.relationship(secondary=stream_schedule, back_populates='streams')

class Schedule(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[Optional[str]] = so.mapped_column(
            sa.String(128),
            comment="title for the stream"
        )
    day_of_week: so.Mapped[int] = so.mapped_column(
            comment="day of week the stream will run on"
        )
    start_time: so.Mapped[int] = so.mapped_column(
            comment="time of day that the stream should start"
        )
    duration: so.Mapped[int] = so.mapped_column(
            comment="duration in minutes that the stream should run",
            default=150 # 2.5 hours
        )
    repeat_until: so.Mapped[Optional[int]] = so.mapped_column(
            comment="timestamp: if the stream should stop after a certain date"
        )
    active: so.Mapped[bool] = so.mapped_column(
            comment="If this schedule is currently active",
            default=True
        )
    run_once: so.Mapped[bool] = so.mapped_column(
            comment="If this schedule should only run once",
            default=False
        )

    streams: so.Mapped[List[Stream]] = so.relationship(secondary=stream_schedule, back_populates='schedules')
