from sqlalchemy.orm import Session
import uuid

from app.models.customer import Customer
from app.core.exceptions import AppException
from app.core.security import create_access_token, create_refresh_token


def register_and_login_customer(db: Session, data):
    
    # Email already exists (not deleted)
    email_exists = db.query(Customer).filter(
        Customer.email == data.email,
        Customer.is_delete == False
    ).first()

    if email_exists:
        raise AppException(
            status=400,
            message="Email already registered"
        )

    # Contact already exists (not deleted)
    contact_exists = db.query(Customer).filter(
        Customer.contact == data.contact,
        Customer.is_delete == False
    ).first()

    if contact_exists:
        raise AppException(
            status=400,
            message="Contact number already registered"
        )

    customer = Customer(
        uu_id=str(uuid.uuid4()),
        name=data.name,
        email=data.email,
        contact=data.contact,
        is_active=True
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    # JWT payload (same pattern as admin)
    payload = {
        "user_id": customer.id,
        "email": customer.email,
        "name": customer.name,
        "contact": customer.contact,
        "profile_image": None
    }

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer",
        "user": {
            "id": customer.id,
            "email": customer.email,
            "name": customer.name,
            "contact": customer.contact,
            "profile_image": None,
            "is_admin": False,
            "uu_id": customer.uu_id,
            "is_active": customer.is_active
        }
    }
