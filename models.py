from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DECIMAL,
    TIMESTAMP,
    ForeignKey,
    Enum,
    create_engine,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#mysql shell 설치
#mysqlconnector intsall


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:rlarmadud123!@localhost/dart"
#개별 mysql 로컬 비밀번호로 바꿔야함

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    email = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class Account(Base):
    __tablename__ = "account"
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    userEmail = Column(String(255), ForeignKey("user.email", ondelete="CASCADE"))
    account_name = Column(String(255), nullable=False)
    deposit = Column(DECIMAL(15, 2), default=0.0)
    currency_id = Column(
        Integer, ForeignKey("currency.id"), nullable=False
    )  # currency 관계


class Investment(Base):
    __tablename__ = "investment"
    investment_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.account_id", ondelete="CASCADE"))
    stock_symbol = Column(String(50))
    quantity = Column(Float, nullable=False)
    purchase_price = Column(DECIMAL(10, 2), nullable=False)
    current_price = Column(DECIMAL(10, 2), nullable=False)
    total_value = Column(DECIMAL(15, 2))
    currency_id = Column(
        Integer, ForeignKey("currency.id"), nullable=False
    )  # currency 관계


class Transaction(Base):
    __tablename__ = "transaction"
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.account_id", ondelete="CASCADE"))
    stock_symbol = Column(String(50))
    transaction_type = Column(Enum("BUY", "SELL"), nullable=False)
    quantity = Column(Float, nullable=False)
    buysell_price = Column(DECIMAL(10, 2), nullable=False)
    transaction_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    currency_id = Column(
        Integer, ForeignKey("currency.id"), nullable=False
    )  # currency 관계


class AccountHistory(Base):
    __tablename__ = "account_history"
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("account.account_id", ondelete="CASCADE"))
    updated_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    total_value = Column(DECIMAL(15, 2), nullable=False)
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)  # currency 관계

class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_code = Column(
        String(10), unique=True, nullable=False
    )  # 화폐코드 USD,EUR,KRW
    exchange_rate = Column(DECIMAL(10, 4), nullable=False)  # 1 USD 기준 환율


Base.metadata.create_all(bind=engine)
