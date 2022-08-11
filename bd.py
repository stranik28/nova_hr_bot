from calendar import calendar
from sqlite3 import connect
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean,update, Float
import pymysql

async def connect():
    engine = create_engine("mysql+pymysql://stranik:n01082002@localhost/nova")
    engine.connect()
    return engine

metadata = MetaData()

rev = Table('rev', metadata,
    Column('id', Integer, primary_key=True),
    Column('calendar', String(50)),
    Column('fio', String(50)),
    Column('Skills', String(50)),
    Column('Type_of_work', String(50)),
    Column('Level', String(50)),
    Column('hard', Float),
    Column('soft', Float),
    Column('full_Artemsm67', Text),
    Column('full_reaL_IdpNik', Text),
    Column('full_cris_tee', Text),
    Column('full_foxyess2020', Text),
    Column('hard_foxyess2020', Integer),
    Column('hard_Artemsm67', Integer),
    Column('hard_reaL_IdpNik', Integer),
    Column('hard_cris_tee', Integer),
    Column('soft_Artemsm67', Integer),
    Column('soft_reaL_IdpNik', Integer),
    Column('soft_cris_tee', Integer),
    Column('soft_foxyess2020', Integer),
    Column('date', DateTime),
    Column('record', String(128))
)

def create_table():
    engine = create_engine("mysql+pymysql://stranik:n01082002@localhost/nova")
    engine.connect()
    metadata.create_all(engine)

async def check(vv):
    # print(vv)
    engine = await connect()
    datas = rev.select().where(rev.c.calendar == vv)
    data = engine.execute(datas).rowcount
    # print(data)
    if data == 0:
        ins = rev.insert().values(calendar = vv)
        engine.execute(ins)
    return

async def insert_val_min(val):
    engine = await connect()
    await check(val[1])
    if val[0] == "Artemsm67":
        ins = update(rev).where(rev.c.calendar == val[1]).values(full_Artemsm67=val[2], hard_Artemsm67=val[3],soft_Artemsm67=val[4])
    elif val[0] == "reaL_IdpNik":
        ins = update(rev).where(rev.c.calendar == val[1]).values(full_reaL_IdpNik=val[2], hard_reaL_IdpNik=val[3],soft_reaL_IdpNik=val[4])
    elif val[0] == "cris_tee":
        ins = update(rev).where(rev.c.calendar == val[1]).values(full_cris_tee=val[2], hard_cris_tee=val[3],soft_cris_tee=val[4])
    elif val[0] == "foxyess2020":
        ins = update(rev).where(rev.c.calendar == val[1]).values(full_foxyess2020=val[2], hard_foxyess2020=val[3],soft_foxyess2020=val[4])
    engine.execute(ins)
    engine.dispose()
    await update_datas(val[1])

async def add_video(vid):
    engine = await connect()
    await check(vid[0])
    ins = update(rev).where(rev.c.calendar == vid[0]).values(record = vid[1])
    engine.execute(ins)
    engine.dispose()

async def update_datas(info):
    engine = await connect()
    ins = rev.select().where(rev.c.calendar == info[0])
    data = engine.execute(ins)
    print(data)
    print(ins)
