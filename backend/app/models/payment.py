"""
支付和积分模型
"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class CreditPackage(Base):
    """积分套餐表"""

    __tablename__ = "credit_packages"

    id = Column(String, primary_key=True)  # 如 "popular"
    name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="USD")
    stripe_price_id = Column(String, nullable=True)
    is_popular = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TransactionType(str, enum.Enum):
    """交易类型"""

    PURCHASE = "purchase"
    CONSUMPTION = "consumption"
    REFUND = "refund"
    BONUS = "bonus"


class CreditTransaction(Base):
    """积分交易表"""

    __tablename__ = "credit_transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    amount = Column(Integer, nullable=False)  # 正数增加，负数扣除
    balance_before = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    stripe_session_id = Column(String, nullable=True)
    stripe_payment_intent_id = Column(String, nullable=True)
    related_job_id = Column(String, ForeignKey("generation_jobs.id"), nullable=True)
    extra_data = Column(String, nullable=True)  # JSON string

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StripeEvent(Base):
    """Stripe 事件表（用于幂等性）"""

    __tablename__ = "stripe_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String, unique=True, nullable=False)  # Stripe Event ID
    event_type = Column(String, nullable=False)
    processed = Column(Boolean, default=False)
    payload = Column(String, nullable=True)  # JSON string

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
