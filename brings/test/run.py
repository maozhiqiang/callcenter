
from database import init_db,db_session
from models import User
# init_db()
# u = User('admin1123', 'admin@localhost123122')
# db_session.add(u)
# db_session.commit()
def ss():
    u  = User.query.filter(User.name == 'admin').first()
    print u


if __name__ == '__main__':
    ss()