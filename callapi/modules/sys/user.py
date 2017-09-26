from callapi.app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=False)
    phone = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80),unique=False)
    source = db.Column(db.Integer,unique=False)
    terminal = db.Column(db.Integer,unique=False)
    invited_from = db.Column(db.String(80),unique=False)

    #重写该方法，方便输出user信息
    def __repr__(self):
        user = ''
        user += 'name: %s\n' % (self.name)
        user += 'phone: %s\n' % (self.phone)
        user += 'password: %s\n' % (self.password)
        return user

    def create_user(phone,password,invited_from,terminal):
        user = User(phone=phone,password=password,terminal=terminal,invited_from=invited_from)
        db.session.add(user)
        try:
            db.session.commit()
        except BaseException:
            return 0
        else:
            return user.id
