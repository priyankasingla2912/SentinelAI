from enum import StrEnum


class Role(StrEnum):
    ADMIN = "ADMIN"
    SENIOR_FRAUD_ANALYST = "SENIOR_FRAUD_ANALYST"
    FRAUD_ANALYST = "FRAUD_ANALYST"
    VIEWER = "VIEWER"


class Permission(StrEnum):
    VIEW_DASHBOARDS = "VIEW_DASHBOARDS"
    VIEW_PREDICTION_HISTORY = "VIEW_PREDICTION_HISTORY"
    VIEW_ALL_CASES = "VIEW_ALL_CASES"
    VIEW_ASSIGNED_CASES = "VIEW_ASSIGNED_CASES"
    CREATE_PREDICTIONS = "CREATE_PREDICTIONS"
    CREATE_CASES = "CREATE_CASES"
    INVESTIGATE_FRAUD = "INVESTIGATE_FRAUD"
    ASSIGN_CASES = "ASSIGN_CASES"
    UPDATE_ALL_CASES = "UPDATE_ALL_CASES"
    UPDATE_ASSIGNED_CASES = "UPDATE_ASSIGNED_CASES"
    MANAGE_USERS = "MANAGE_USERS"
    VIEW_AUDIT_LOGS = "VIEW_AUDIT_LOGS"


ROLE_PERMISSIONS = {
    Role.ADMIN: set(Permission),

    Role.SENIOR_FRAUD_ANALYST: {
        Permission.VIEW_DASHBOARDS,
        Permission.VIEW_PREDICTION_HISTORY,
        Permission.VIEW_ALL_CASES,
        Permission.VIEW_ASSIGNED_CASES,
        Permission.CREATE_PREDICTIONS,
        Permission.CREATE_CASES,
        Permission.INVESTIGATE_FRAUD,
        Permission.ASSIGN_CASES,
        Permission.UPDATE_ALL_CASES,
    },

    Role.FRAUD_ANALYST: {
        Permission.VIEW_DASHBOARDS,
        Permission.VIEW_PREDICTION_HISTORY,
        Permission.VIEW_ASSIGNED_CASES,
        Permission.CREATE_PREDICTIONS,
        Permission.CREATE_CASES,
        Permission.INVESTIGATE_FRAUD,
        Permission.UPDATE_ASSIGNED_CASES,
    },

    Role.VIEWER: {
        Permission.VIEW_DASHBOARDS,
        Permission.VIEW_PREDICTION_HISTORY,
        Permission.VIEW_ALL_CASES,
    },
}


def has_permission(role: str, permission: Permission) -> bool:
    try:
        normalized_role = Role(role)
    except ValueError:
        return False

    return permission in ROLE_PERMISSIONS[normalized_role]