from calendar import calendar
from sqlite3 import connect
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean,update, Float
import pymysql
import datetime

async def connect():
    engine = create_engine("mysql+pymysql://stranik:n01082002@localhost/nova")
    engine.connect()
    return engine

metadata = MetaData()

rev = Table('rev', metadata,
    Column('id', Integer, primary_key=True), #0
    Column('calendar', String(50)), #1
    Column('fio', String(128)), #2
    Column('Education', String(128)), #3
    Column('Skills', String(50)), #4
    Column('Type_of_work', String(50)), #5
    Column('Experience', String(50)), #6
    Column('Level', String(50)), #7
    Column('hard', Float), #8
    Column('soft', Float), #9
    Column('full_Artemsm67', Text), #10
    Column('full_reaL_IdpNik', Text), #11
    Column('full_cris_tee', Text), #12
    Column('full_foxyess2020', Text), #13
    Column('hard_foxyess2020', Integer), #14
    Column('hard_Artemsm67', Integer), #15
    Column('hard_reaL_IdpNik', Integer), #16
    Column('hard_cris_tee', Integer), #17
    Column('soft_Artemsm67', Integer), #18
    Column('soft_reaL_IdpNik', Integer), #19
    Column('soft_cris_tee', Integer), #20
    Column('soft_foxyess2020', Integer), #21
    Column('date', DateTime, default = datetime.datetime.now()), #22
    Column('record', String(128)) #23
)

def create_table():
    engine = create_engine("mysql+pymysql://stranik:n01082002@localhost/nova")
    engine.connect()
    metadata.create_all(engine)

async def check(vv):
    engine = await connect()
    datas = rev.select().where(rev.c.calendar == vv)
    data = engine.execute(datas).rowcount
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

async def isNanC(val):
    if (val != val) or (val is None):
        return False
    else:
        return True

async def update_datas(info):
    engine = await connect()
    ins = rev.select().where(rev.c.calendar == info)
    data = engine.execute(ins).fetchall()
    hard1 = (data[0][14]) if await isNanC(data[0][14]) else 0
    hard2 = (data[0][15]) if await isNanC(data[0][15]) else 0
    hard3 = (data[0][16]) if await isNanC(data[0][16]) else 0
    hard4 = (data[0][17]) if await isNanC(data[0][17]) else 0
    soft1 = (data[0][18]) if await isNanC(data[0][18]) else 0
    soft2 = (data[0][19]) if await isNanC(data[0][19]) else 0
    soft3 = (data[0][20]) if await isNanC(data[0][20]) else 0
    soft4 = (data[0][21]) if await isNanC(data[0][21]) else 0
    hard = int(hard1) + int(hard2) + int(hard3) + int(hard4)
    hard = hard/4
    soft = int(soft1) + int(soft2) + int(soft3) + int(soft4)
    soft = soft/4
    ins = update(rev).where(rev.c.calendar == info[0]).values(hard=hard, soft = soft)
    engine.execute(ins)
    engine.dispose()

async def update_info(sobes,type,text,usr):
    await check(sobes)
    type = int(type)
    if type == 0:
        engine = await connect()
        ins = update(rev).where(rev.c.calendar == sobes).values(fio=text)
        engine.execute(ins)
        engine.dispose()
    elif type == 1:
        engine = await connect()
        ins = update(rev).where(rev.c.calendar == sobes).values(Skills=text)
        engine.execute(ins)
        engine.dispose()
    elif type == 2:
        engine = await connect()
        ins = update(rev).where(rev.c.calendar == sobes).values(Education=text)
        engine.execute(ins)
        engine.dispose()
    elif type == 3:
        engine = await connect()
        ins = update(rev).where(rev.c.calendar == sobes).values(Type_of_work=text)
        engine.execute(ins)
        engine.dispose()
    elif type == 4:
        engine = await connect()
        ins = update(rev).where(rev.c.calendar == sobes).values(Experience=text)
        engine.execute(ins)
        engine.dispose()
    elif type == 5:
        engine = await connect()
        ins = update(rev).where(rev.c.calendar == sobes).values(Level=text)
        engine.execute(ins)
        engine.dispose()
    elif type == 6:
        engine = await connect()
        if usr == "Artemsm67":
            ins = update(rev).where(rev.c.calendar == sobes).values(hard_Artemsm67=text)
        elif usr == "reaL_IdpNik":
            ins = update(rev).where(rev.c.calendar == sobes).values(hard_reaL_IdpNik=text)
        elif usr == "cris_tee":
            ins = update(rev).where(rev.c.calendar == sobes).values(hard_cris_tee=text)
        elif usr == "foxyess2020":
            ins = update(rev).where(rev.c.calendar == sobes).values(hard_foxyess2020=text)
        engine.execute(ins)
        engine.dispose()
    elif type == 7:
        engine = await connect()
        if usr == "Artemsm67":
            ins = update(rev).where(rev.c.calendar == sobes).values(soft_Artemsm67=text)
        elif usr == "reaL_IdpNik":
            ins = update(rev).where(rev.c.calendar == sobes).values(soft_reaL_IdpNik=text)
        elif usr == "cris_tee":
            ins = update(rev).where(rev.c.calendar == sobes).values(soft_cris_tee=text)
        elif usr == "foxyess2020":
            ins = update(rev).where(rev.c.calendar == sobes).values(soft_foxyess2020=text)
        engine.execute(ins)
        engine.dispose()
    elif type == 8:
        engine = await connect()
        if usr == "Artemsm67":
            ins = update(rev).where(rev.c.calendar == sobes).values(full_Artemsm67=text)
        elif usr == "reaL_IdpNik":
            ins = update(rev).where(rev.c.calendar == sobes).values(full_reaL_IdpNik=text)
        elif usr == "cris_tee":
            ins = update(rev).where(rev.c.calendar == sobes).values(full_cris_tee=text)
        elif usr == "foxyess2020":
            ins = update(rev).where(rev.c.calendar == sobes).values(full_foxyess2020=text)
        engine.execute(ins)
        engine.dispose()
    await update_datas(sobes)


create_table()
