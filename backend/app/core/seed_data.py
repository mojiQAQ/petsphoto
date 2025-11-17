"""
种子数据脚本
"""
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models import GenerationStyle, CreditPackage, User
from datetime import datetime


def create_generation_styles(db: Session):
    """创建预设风格数据"""
    styles = [
        {
            "id": "cartoon",
            "name": "卡通风格",
            "description": "色彩鲜艳的卡通画风",
            "prompt_template": "cartoon style, vibrant colors, cute pet illustration",
            "sort_order": 1,
        },
        {
            "id": "oil_painting",
            "name": "油画风格",
            "description": "经典艺术油画效果",
            "prompt_template": "oil painting style, artistic, classical portrait",
            "sort_order": 2,
        },
        {
            "id": "watercolor",
            "name": "水彩风格",
            "description": "柔和的水彩画效果",
            "prompt_template": "watercolor painting, soft colors, gentle brush strokes",
            "sort_order": 3,
        },
        {
            "id": "pixel_art",
            "name": "像素艺术",
            "description": "复古像素游戏风格",
            "prompt_template": "pixel art, 8-bit style, retro gaming aesthetic",
            "sort_order": 4,
        },
        {
            "id": "cyberpunk",
            "name": "赛博朋克",
            "description": "未来科幻霓虹风格",
            "prompt_template": "cyberpunk style, neon lights, futuristic pet portrait",
            "sort_order": 5,
        },
    ]

    for style_data in styles:
        existing = db.query(GenerationStyle).filter_by(id=style_data["id"]).first()
        if not existing:
            style = GenerationStyle(**style_data)
            db.add(style)

    db.commit()
    print(f"✅ Created {len(styles)} generation styles")


def create_credit_packages(db: Session):
    """创建积分套餐数据"""
    packages = [
        {
            "id": "basic",
            "name": "基础套餐",
            "credits": 10,
            "price": Decimal("4.99"),
            "is_popular": False,
            "sort_order": 1,
        },
        {
            "id": "popular",
            "name": "热门套餐",
            "credits": 30,
            "price": Decimal("12.99"),
            "is_popular": True,
            "sort_order": 2,
        },
        {
            "id": "value",
            "name": "超值套餐",
            "credits": 100,
            "price": Decimal("39.99"),
            "is_popular": False,
            "sort_order": 3,
        },
        {
            "id": "enterprise",
            "name": "企业套餐",
            "credits": 300,
            "price": Decimal("99.99"),
            "is_popular": False,
            "sort_order": 4,
        },
    ]

    for package_data in packages:
        existing = db.query(CreditPackage).filter_by(id=package_data["id"]).first()
        if not existing:
            package = CreditPackage(**package_data)
            db.add(package)

    db.commit()
    print(f"✅ Created {len(packages)} credit packages")


def create_guest_user(db: Session):
    """创建访客用户用于 MVP 开发"""
    guest_id = "guest"
    existing = db.query(User).filter_by(id=guest_id).first()

    if not existing:
        guest = User(
            id=guest_id,
            email="guest@petsphoto.local",
            credits=999999,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(guest)
        db.commit()
        print(f"✅ Created guest user with unlimited credits")
    else:
        print(f"ℹ️  Guest user already exists")


def seed_database(db: Session):
    """运行所有种子数据"""
    print("🌱 Seeding database...")
    create_guest_user(db)
    create_generation_styles(db)
    create_credit_packages(db)
    print("✅ Database seeding completed")


if __name__ == "__main__":
    from app.core.database import SessionLocal

    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
