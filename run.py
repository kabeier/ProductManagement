from app import db, create_app

from app.blueprints.authentication.models import User, UserRole
from app.blueprints.shop.models import Category, Product

app = create_app()


@app.shell_context_processor
def make_context():
    return dict(db=db, User=User, UserRole=UserRole, Category=Category, Product=Product)
