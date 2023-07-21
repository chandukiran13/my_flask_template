# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from typing import Optional, Type, TypeVar

from .extensions import db, cache

T = TypeVar("T", bound="PkModel")

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""
    __abstract__ = True
    cacheable = False

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit: bool = True) -> None:
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            return db.session.commit()
        return


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    id = Column(db.String, primary_key=True)
    __abstract__ = True

    @classmethod
    def get_by_id(cls: Type[T], record_id) -> Optional[T]:
        """Get record by ID."""
        if isinstance(record_id, (int, float)):
            return cls.query.get(int(record_id))
        return None

    @classmethod
    def load(cls, id):
        if cls.cacheable:
            return cls._fetch(id)
        else:
            return cls.get_by_id(id)

    @classmethod
    def load_all(cls):
        if cls.cacheable:
            return cls._fetch_all()
        else:
            return cls.query.all()

    @classmethod
    @cache.memoize(300)
    def _fetch(cls, id):
        return cls.query.get(id)

    @classmethod
    @cache.memoize(3000)
    def _fetch_all(cls):
        """Caches all the objects in a query if only it's cacheable"""
        return cls.query.all()

    def invalidate_cache(self):
        cache.delete_memoized(self.fetch, self.id)

    def delete(self, commit=True):
        if self.cacheable:
            self.invalidate_cache()
        return super().delete(commit)

    def update(self, commit=True, **kwargs):
        if self.cacheable:
            self.invalidate_cache()
        return super().update(commit, **kwargs)


def reference_col(
    tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )
