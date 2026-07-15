from typing import Optional, Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session, select

# --- 第一部分：数据建模 (Data Structuring) ---
# SQLModel 同时继承了 Pydantic.BaseModel 和 SQLAlchemy.declarative_base
class Hero(SQLModel, table=True):
    # table=True 声明这不仅是一个 Pydantic 模型，还是一个数据库表
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # Pydantic 校验与数据库索引同步定义
    secret_name: str
    age: Optional[int] = None

# --- 第二部分：引擎与运行环境 (Execution Engine) ---
sqlite_url = "sqlite:///database.db"
# create_engine 是连接 Python 解释器与底层数据库的桥梁
engine = create_engine(sqlite_url)

def create_db_and_tables():
    # 自动读取所有标注了 table=True 的类并创建表
    SQLModel.metadata.create_all(engine)

# --- 第三部分：Web 服务集成 (Web & Service) ---
app = FastAPI()

# 利用 lifespan 机制管理数据库连接池的启动
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 依赖注入 (Depends) 实现数据库 Session 的自动化管理
def get_session():
    with Session(engine) as session:
        yield session

@app.post("/heroes/", response_model=Hero)
def create_hero(
    hero: Hero, # 此处 hero 作为 Pydantic 模型自动执行输入验证
    session: Annotated[Session, Depends(get_session)] # 依赖注入 Session
):
    # 此处 hero 作为 ORM 对象直接保存到数据库
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes/", response_model=list[Hero])
def read_heroes(session: Annotated[Session, Depends(get_session)]):
    heroes = session.exec(select(Hero)).all()
    return heroes