import os

from Catalog import create_app, db

from Catalog.models import User, LoginUser, Category, Item

from flask.ext.script import Manager, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('CATALOG_ENV') or 'dev')
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def seedDB():

    db.session.add(Category(title="Soccer"))  # 1
    db.session.add(Category(title="Basketball"))  # 2
    db.session.add(Category(title="Baseball"))  # 3
    db.session.add(Category(title="Frisbee"))  # 4
    db.session.add(Category(title="Snowboarding"))  # 5
    db.session.add(Category(title="Rock Climbing"))  # 6
    db.session.add(Category(title="Foosball"))  # 7
    db.session.add(Category(title="Skating"))  # 8
    db.session.add(Category(title="Hockey"))  # 9

    def addUser(name, email, picture):
        db.session.add(User(name=name, picture=picture, email=email))

    addUser('Bill the Cat', 'billthecat@example.com',
            'http://i83.photobucket.com/albums/j291/RTCCHEUNG/cat-hat.jpg')
    addUser('Earthworm Jim', 'eatDirt@underground.net',
            'http://img09.deviantart.net/1b03/i/2006/276/8/4/earthworm_jim_by_blackberet.jpg')

    BillyBob = LoginUser(username="billthecat", password="testing", user_id=1)
    Crash = LoginUser(username="jimworm", password="testing", user_id=2)
    db.session.add(BillyBob)
    db.session.add(Crash)

    db.session.add(Item(name="Soccer Ball",
                        description="They must be delivered safely or other star systems will suffer the same fate as Alderaan. Your destiny lies along a different path than mine. The Force will be with you...always! Boy you said it, Chewie. Where did you dig up that old fossil? Ben is a great man. Yeah, great at getting us into trouble. I didn't hear you give any ideas... Well, anything would be better than just hanging around waiting for him to pick us up... Who do you think...",
                        user_id="1",
                        category_id="1"))

    db.session.add(Item(name="Ice Skates",
                        description="The battle station is heavily shielded and carries a firepower greater than half the star fleet. It's defenses are designed around a direct large-scale assault. A small one-man fighter should be able to penetrate the outer defense. Pardon me for asking, sir, but what good are snub fighters going to be against that? Well, the Empire doesn't consider a small one-man fighter to be any threat, or they'd have a tighter defense. An analysis of the plans provided by Princess Leia has demonstrated a weakness in the battle station.",
                        user_id="1",
                        photo_path='cliched_exchanges.png',
                        category_id="8"))

    db.session.add(Item(name="Baseball bat",
                        description="They must be delivered safely or other star systems will suffer the same fate as Alderaan. Your destiny lies along a different path than mine. The Force will be with you...always! Boy you said it, Chewie. Where did you dig up that old fossil? Ben is a great man. Yeah, great at getting us into trouble. I didn't hear you give any ideas... Well, anything would be better than just hanging around waiting for him to pick us up... Who do you think...",
                        user_id="2",
                        photo_path='flowchart.jpg',
                        category_id="3"))

    db.session.add(Item(name="Innova Cheetah",
                        description="Someone was in the pod. The tracks go off in this direction. Look, sir -- droids.",
                        user_id="1",
                        photo_path='python.jpg',
                        category_id="4"))

    db.session.add(Item(name="Cleats",
                        description="Luke, take these two over to the garage, will you? I want you to have both of them cleaned up before dinner. But I was going into Toshi Station to pick up some power converters... You can waste time with your friends when your chores are done. Now come on, get to it! All right, come on! And the red one, come on. Well, come on, Red, let's go.",
                        user_id="2",
                        category_id="5"))

    db.session.add(Item(name="Bantha Fodder",
                        description="Uncle Owen... Yeah?This R2 unit has a bad motivator. Look! Hey, what're you trying to push on us? Excuse me, sir, but that R2 unit is in prime condition. A real bargain. Uncle Owen... Yeah? What about that one? What about that blue one? We'll take that one. Yeah, take it away.",
                        user_id="2",
                        category_id="6"))

    db.session.add(Item(name="Harness",
                        description="Artoo? Artoo! Where are you?",
                        user_id="2",
                        category_id="7"))

    db.session.add(Item(name="Rhinestones",
                        description="Noisy brute. Why don't we just go into light-speed? We can't? How would you know the hyperdrive is deactivated? The city's central computer told you? Artoo-Detoo, you know better than to trust a strange computer. Ouch! Pay attention to what you're doing!",
                        user_id="1",
                        photo_path='xkcd.jpg',
                        category_id="8"))

    db.session.add(Item(name="Puck",
                        description="Bring me Solo and the Wookiee. They will all suffer for this outrage.",
                        user_id="2",
                        photo_path='xkcd2.png',
                        category_id="9"))

    db.session.commit()
    print 'Seeded the database'


@manager.command
def dropdb():
    if prompt_bool(
            "Are you sure you want to drop all of your data?"):
        db.drop_all()
        print "Dropped the database"


if __name__ == '__main__':
    manager.run()
