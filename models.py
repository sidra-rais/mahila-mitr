"""
Models Module for Mahila Mitr System
Defines standard classes for the entities used across the system.
"""


class MahilaMitr:
    """Represents a registered Mahila Mitr community volunteer."""

    def __init__(self, mitr_id, name, area, is_available=True, assistance_type="General assistance", phone_demo="N/A", help_count=0):
        self.id = mitr_id
        self.name = name
        self.area = area
        self.is_available = is_available
        self.assistance_type = assistance_type
        self.phone_demo = phone_demo
        self.help_count = help_count

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "area": self.area,
            "is_available": self.is_available,
            "assistance_type": self.assistance_type,
            "phone_demo": self.phone_demo,
            "help_count": self.help_count
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            mitr_id=data.get("id", ""),
            name=data.get("name", ""),
            area=data.get("area", ""),
            is_available=data.get("is_available", True),
            assistance_type=data.get("assistance_type", "General assistance"),
            phone_demo=data.get("phone_demo", "N/A"),
            help_count=data.get("help_count", 0)
        )


class HelpRequest:
    """Represents a support request created by a user."""

    def __init__(self, req_id, user_name, situation, area, urgency, assistance_needed, description, status="Pending", assigned_mitr="None", created_at=""):
        self.id = req_id
        self.user_name = user_name
        self.situation = situation
        self.area = area
        self.urgency = urgency
        self.assistance_needed = assistance_needed
        self.description = description
        self.status = status
        self.assigned_mitr = assigned_mitr
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "situation": self.situation,
            "area": self.area,
            "urgency": self.urgency,
            "assistance_needed": self.assistance_needed,
            "description": self.description,
            "status": self.status,
            "assigned_mitr": self.assigned_mitr,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            req_id=data.get("id", ""),
            user_name=data.get("user_name", ""),
            situation=data.get("situation", ""),
            area=data.get("area", ""),
            urgency=data.get("urgency", "Medium"),
            assistance_needed=data.get("assistance_needed", "General assistance"),
            description=data.get("description", ""),
            status=data.get("status", "Pending"),
            assigned_mitr=data.get("assigned_mitr", "None"),
            created_at=data.get("created_at", "")
        )


class SafetyReport:
    """Represents an unsafe location or incident report submitted by the community."""

    def __init__(self, report_id, area, category, severity, description, date_time="", confirmations=1, status="Reported"):
        self.id = report_id
        self.area = area
        self.category = category
        self.severity = severity
        self.description = description
        self.date_time = date_time
        self.confirmations = confirmations
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "area": self.area,
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "date_time": self.date_time,
            "confirmations": self.confirmations,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            report_id=data.get("id", ""),
            area=data.get("area", ""),
            category=data.get("category", "Other"),
            severity=data.get("severity", "Medium"),
            description=data.get("description", ""),
            date_time=data.get("date_time", ""),
            confirmations=data.get("confirmations", 1),
            status=data.get("status", "Reported")
        )


class User:
    """Represents a standard community user profile."""

    def __init__(self, user_id, name, area, role="User", registered_date=""):
        self.id = user_id
        self.name = name
        self.area = area
        self.role = role
        self.registered_date = registered_date

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "area": self.area,
            "role": self.role,
            "registered_date": self.registered_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get("id", ""),
            name=data.get("name", ""),
            area=data.get("area", ""),
            role=data.get("role", "User"),
            registered_date=data.get("registered_date", "")
        )
