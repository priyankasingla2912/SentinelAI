import pytest

from app.roles import Role, Permission, has_permission


@pytest.mark.parametrize("permission", list(Permission))
def test_admin_has_all_permissions(permission):
    assert has_permission(Role.ADMIN, permission)


@pytest.mark.parametrize(
    "permission",
    [
        Permission.VIEW_DASHBOARDS,
        Permission.VIEW_PREDICTION_HISTORY,
        Permission.VIEW_ALL_CASES,
        Permission.VIEW_ASSIGNED_CASES,
        Permission.CREATE_PREDICTIONS,
        Permission.CREATE_CASES,
        Permission.INVESTIGATE_FRAUD,
        Permission.ASSIGN_CASES,
        Permission.UPDATE_ALL_CASES,
    ],
)
def test_senior_analyst_permissions(permission):
    assert has_permission(Role.SENIOR_FRAUD_ANALYST, permission)


@pytest.mark.parametrize(
    "permission",
    [
        Permission.VIEW_DASHBOARDS,
        Permission.VIEW_PREDICTION_HISTORY,
        Permission.VIEW_ASSIGNED_CASES,
        Permission.CREATE_PREDICTIONS,
        Permission.CREATE_CASES,
        Permission.INVESTIGATE_FRAUD,
        Permission.UPDATE_ASSIGNED_CASES,
    ],
)
def test_fraud_analyst_permissions(permission):
    assert has_permission(Role.FRAUD_ANALYST, permission)


@pytest.mark.parametrize(
    "permission",
    [
        Permission.VIEW_DASHBOARDS,
        Permission.VIEW_PREDICTION_HISTORY,
        Permission.VIEW_ALL_CASES,
    ],
)
def test_viewer_permissions(permission):
    assert has_permission(Role.VIEWER, permission)


@pytest.mark.parametrize(
    "role,permission",
    [
        (Role.SENIOR_FRAUD_ANALYST, Permission.MANAGE_USERS),
        (Role.SENIOR_FRAUD_ANALYST, Permission.VIEW_AUDIT_LOGS),
        (Role.FRAUD_ANALYST, Permission.VIEW_ALL_CASES),
        (Role.FRAUD_ANALYST, Permission.ASSIGN_CASES),
        (Role.FRAUD_ANALYST, Permission.UPDATE_ALL_CASES),
        (Role.VIEWER, Permission.CREATE_CASES),
        (Role.VIEWER, Permission.CREATE_PREDICTIONS),
        (Role.VIEWER, Permission.UPDATE_ALL_CASES),
        (Role.VIEWER, Permission.UPDATE_ASSIGNED_CASES),
        (Role.VIEWER, Permission.MANAGE_USERS),
    ],
)
def test_restricted_permissions(role, permission):
    assert not has_permission(role, permission)


def test_unknown_role_has_no_permissions():
    assert not has_permission("UNKNOWN_ROLE", Permission.VIEW_DASHBOARDS)
