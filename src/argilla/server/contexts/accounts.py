#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from uuid import UUID

from argilla.server.models import User, UserWorkspace, Workspace
from argilla.server.security.model import (
    UserCreate,
    UserWorkspaceCreate,
    WorkspaceCreate,
)
from passlib.context import CryptContext
from sqlalchemy.orm import Session

_CRYPT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_workspace_by_user_id_and_workspace_id(db: Session, user_id: UUID, workspace_id: UUID):
    return (
        db.query(UserWorkspace)
        .filter(
            UserWorkspace.user_id == user_id,
            UserWorkspace.workspace_id == workspace_id,
        )
        .first()
    )


def create_user_workspace(db: Session, user_workspace_create: UserWorkspaceCreate):
    user_workspace = UserWorkspace(
        user_id=user_workspace_create.user_id, workspace_id=user_workspace_create.workspace_id
    )

    db.add(user_workspace)
    db.commit()
    db.refresh(user_workspace)

    return user_workspace


def delete_user_workspace(db: Session, user_workspace: UserWorkspace):
    db.delete(user_workspace)
    db.commit()

    return user_workspace


def get_workspace_by_id(db: Session, workspace_id: UUID):
    return db.query(Workspace).get(workspace_id)


def list_workspaces(db: Session):
    return db.query(Workspace).order_by(Workspace.inserted_at.asc()).all()


def create_workspace(db: Session, workspace_create: WorkspaceCreate):
    workspace = Workspace(name=workspace_create.name)

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    return workspace


def delete_workspace(db: Session, workspace: Workspace):
    db.delete(workspace)
    db.commit()

    return workspace


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).get(user_id)


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_api_key(db: Session, api_key: str):
    return db.query(User).filter(User.api_key == api_key).first()


def list_users(db: Session):
    return db.query(User).order_by(User.inserted_at.asc()).all()


def create_user(db: Session, user_create: UserCreate):
    user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        username=user_create.username,
        password_hash=_CRYPT_CONTEXT.hash(user_create.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

    return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)

    if user and _CRYPT_CONTEXT.verify(password, user.password_hash):
        return user
    elif user:
        return
    else:
        _CRYPT_CONTEXT.verify_dummy()