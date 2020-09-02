import os
from serv import create_app, db
from serv.models import User, Section, Site
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(
        db          = db,
        User        = User,
        Site        = Site,
        Section     = Section
    )

@app.cli.command()
def test():
    """Run the unit tests."""
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)