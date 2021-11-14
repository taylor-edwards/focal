"""
Flask app with GraphQL interface to underlying
Postgres database connected with SQLAlchemy
"""

from flask import Flask
from flask_graphql import GraphQLView
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from model import Base
from schema import schema

engine = create_engine('postgresql+psycopg2://focal:asdf@127.0.0.1:5432/focal')
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base.query = db_session.query_property()

app = Flask(__name__)
app.debug = True
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Disconnect database session on shutdown"""
    if exception:
        print(exception)
    db_session.remove()

if __name__ == '__main__':
    app.run()
