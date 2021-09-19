from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Float

engine = create_engine('sqlite:///db.sqlite3', echo=True)
metadata = MetaData()
metadata.bind = engine

moves = []
for i in range(151):
    nullable = i != 0
    moves.append(Column(f"move_{i}", Integer, nullable=nullable))

games = Table(
    'games', metadata,
    Column('id', Integer, primary_key=True),
    Column('event_name', String),
    Column('game_name', String),
    Column('place_name', String),
    Column('game_datetime', DateTime),
    Column('black_player', String),
    Column('white_player', String),
    Column('komi', Float),
    Column('board_size', Integer),
    Column('result', Integer),
    Column('winner', Integer),
    *moves
)
