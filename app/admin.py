from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.extensions import db
from app.models import User, Game, Profile, UserLibrary, WishlistItem, Order, OrderItem

admin_panel = Admin(name='Admin Panel', template_mode='bootstrap4')


class UserView(ModelView):
    column_list = [
        c.name for c in User.__table__.columns if not c == "password"]
    form_columns = [c.name for c in User.__table__.columns]  # type: ignore


class ProfileView(ModelView):
    column_list = [c.name for c in Profile.__table__.columns]  # type: ignore
    form_columns = [c.name for c in Profile.__table__.columns]  # type: ignore


class GameView(ModelView):
    column_list = [c.name for c in Game.__table__.columns]  # type: ignore
    form_columns = [c.name for c in Game.__table__.columns]  # type: ignore


class UserLibraryView(ModelView):
    column_list = [c.name for c in UserLibrary.__table__.columns]  # type: ignore
    form_columns = [c.name for c in UserLibrary.__table__.columns]  # type: ignore


class OrderView(ModelView):
    column_list = [c.name for c in Order.__table__.columns]  # type: ignore
    form_columns = [c.name for c in Order.__table__.columns]  # type: ignore


class OrderItemView(ModelView):
    column_list = [c.name for c in OrderItem.__table__.columns]  # type: ignore
    # type: ignore
    form_columns = [c.name for c in OrderItem.__table__.columns]


class WishlistItemView(ModelView):
    # type: ignore
    column_list = [c.name for c in WishlistItem.__table__.columns]
    # type: ignore
    form_columns = [c.name for c in WishlistItem.__table__.columns]


def init_admin(app):
    admin_panel.init_app(app)
    admin_panel.add_view(UserView(User, db.session))
    admin_panel.add_view(ProfileView(Profile, db.session))
    admin_panel.add_view(GameView(Game, db.session))
    admin_panel.add_view(UserLibraryView(UserLibrary, db.session))
    admin_panel.add_view(OrderView(Order, db.session))
    admin_panel.add_view(OrderItemView(OrderItem, db.session))
    admin_panel.add_view(WishlistItemView(WishlistItem, db.session))
    return admin_panel
