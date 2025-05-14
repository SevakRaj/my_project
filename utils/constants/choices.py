from enum import Enum


class Roles(Enum):
    SUPER_ADMIN = "SUPER ADMIN"
    MANAGER = "MANAGER"  
    OPERATOR = "OPERATOR"  
    CUSTOMER = "CUSTOMER" 
    STORE_EXECUTIVE = "STORE EXECUTIVE"
    ACCOUNTANT = "ACCOUNTANT"
    QC = "QC"
    HR = "HR"
    EMPLOYEE = "EMPLOYEE"
    INWARD = "INWARD"
    VENDOR = "VENDOR"


    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def staff_choices(cls):
        return tuple((i.name, i.value) for i in cls if i.value != Roles.BUSINESS_OWNER.value)

    @classmethod
    def business_choices(cls):
        return tuple((i.name, i.value) for i in cls if i.value == Roles.BUSINESS_OWNER.value)
    
    @classmethod
    def get_formatted_role(role):
        if isinstance(role, Roles):
            return role.value.title()  # Converts to Title Case
        return None