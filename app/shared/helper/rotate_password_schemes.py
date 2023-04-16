from app.shared.auth.password_handler import get_password_hash, verify_password
from app.api.user.models import User
from app.api.agent.models import Agent
from app.api.admin.models import Admin


admins = Admin.read_all()
users = User.read_all()
agents = Agent.read_all()

for admin in admins:
    try:
        admin.password = get_password_hash(admin.name + "123")
        admin.session.commit()
    except Exception as e:
        print(e)
        admin.session.rollback()

for user in users:

    try:
        user.password = get_password_hash(user.name + "123")
        user.session.commit()
    except Exception as e:
        print(e)
        user.session.rollback()

for agent in agents:
    try:
        agent.password = get_password_hash(agent.name + "123")
        agent.session.commit()
    except Exception as e:
        print(e)
        agent.session.rollback()
