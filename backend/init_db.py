import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import time

sys.path.insert(0, str(Path(__file__).parent))

from app.database import Base, engine, SessionLocal
from app.models import User, Specimen, Photo, Identification
from app.models.user import UserRole
from app.models.specimen import (
    IdentificationStatus,
    CrystalSystem,
    AcquisitionMethod
)
from app.utils.security import get_password_hash


def wait_for_db():
    max_retries = 30
    retry_interval = 2
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                print("Database connection successful!")
                return True
        except Exception as e:
            print(f"Waiting for database... ({i+1}/{max_retries})")
            time.sleep(retry_interval)
    print("Failed to connect to database after max retries")
    return False


def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("Database already initialized, skipping...")
            return

        print("Creating demo users...")

        admin = User(
            username="admin",
            email="admin@mineral.com",
            hashed_password=get_password_hash("admin123"),
            full_name="张鉴定师",
            phone="13800000001",
            role=UserRole.ADMIN,
            is_active=True,
            bio="资深矿物鉴定专家，从事矿物研究20年",
            created_at=datetime.utcnow() - timedelta(days=365)
        )
        db.add(admin)

        collector1 = User(
            username="collector1",
            email="collector1@mineral.com",
            hashed_password=get_password_hash("123456"),
            full_name="李藏家",
            phone="13800000002",
            role=UserRole.COLLECTOR,
            is_active=True,
            bio="矿物收藏爱好者，收藏经验10年，主攻萤石和黄铁矿",
            created_at=datetime.utcnow() - timedelta(days=200)
        )
        db.add(collector1)

        collector2 = User(
            username="collector2",
            email="collector2@mineral.com",
            hashed_password=get_password_hash("123456"),
            full_name="王石痴",
            phone="13800000003",
            role=UserRole.COLLECTOR,
            is_active=True,
            bio="化石和矿物双重爱好者，专注于中国本土矿物",
            created_at=datetime.utcnow() - timedelta(days=150)
        )
        db.add(collector2)

        collector3 = User(
            username="collector3",
            email="collector3@mineral.com",
            hashed_password=get_password_hash("123456"),
            full_name="赵晶缘",
            phone="13800000004",
            role=UserRole.COLLECTOR,
            is_active=True,
            bio="水晶和宝石收藏家，经常参加各类矿物展",
            created_at=datetime.utcnow() - timedelta(days=100)
        )
        db.add(collector3)

        db.flush()

        print("Creating demo specimens...")
        base_date = datetime.utcnow() - timedelta(days=180)

        specimens_data = [
            {
                "specimen_no": "SP2025010001",
                "name": "紫色八面体萤石",
                "mineral_type": "萤石",
                "variety": "紫色萤石",
                "locality": "湖南省郴州市香花岭",
                "province": "湖南省",
                "country": "中国",
                "mohs_hardness_min": 4.0,
                "mohs_hardness_max": 4.0,
                "crystal_system": CrystalSystem.ISOMETRIC,
                "crystal_form": "八面体",
                "color": "深紫色",
                "luster": "玻璃光泽",
                "transparency": "透明",
                "cleavage": "完全八面体解理",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 3.18,
                "specific_gravity_max": 3.20,
                "size": "8x6x5cm",
                "weight": 320.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=10),
                "price": 1280.0,
                "currency": "CNY",
                "dealer": "香花矿物商行",
                "description": "完美的紫色八面体萤石晶体，透明度极高，颜色浓郁。晶体表面有天然生长纹，底部带有围岩。",
                "notes": "2024年新开采的精品，荧光反应强烈，长波紫外线下发出亮蓝色荧光。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector1.id
            },
            {
                "specimen_no": "SP2025010002",
                "name": "立方体黄铁矿晶簇",
                "mineral_type": "黄铁矿",
                "variety": "愚人金",
                "locality": "湖南省衡阳市耒阳市",
                "province": "湖南省",
                "country": "中国",
                "mohs_hardness_min": 6.0,
                "mohs_hardness_max": 6.5,
                "crystal_system": CrystalSystem.ISOMETRIC,
                "crystal_form": "立方体",
                "color": "浅黄铜色",
                "luster": "金属光泽",
                "transparency": "不透明",
                "cleavage": "不完全",
                "fracture": "贝壳状",
                "streak": "绿黑色",
                "specific_gravity_min": 4.95,
                "specific_gravity_max": 5.10,
                "size": "12x10x8cm",
                "weight": 850.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.MINING,
                "acquisition_date": base_date + timedelta(days=20),
                "price": 0.0,
                "currency": "CNY",
                "dealer": "自行采集",
                "description": "多颗立方体黄铁矿共生晶簇，最大晶体达2cm。晶形完整，金属光泽强烈，与石英共生。",
                "notes": "2024年夏季野外采集，开采于上二叠统煤系地层。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector1.id
            },
            {
                "specimen_no": "SP2025010003",
                "name": "西瓜碧玺",
                "mineral_type": "电气石",
                "variety": "西瓜碧玺",
                "locality": "新疆维吾尔自治区阿勒泰地区",
                "province": "新疆维吾尔自治区",
                "country": "中国",
                "mohs_hardness_min": 7.0,
                "mohs_hardness_max": 7.5,
                "crystal_system": CrystalSystem.TRIGONAL,
                "crystal_form": "三方柱",
                "color": "绿色外皮，粉红色内核",
                "luster": "玻璃光泽",
                "transparency": "半透明",
                "cleavage": "不明显",
                "fracture": "贝壳状至参差状",
                "streak": "白色",
                "specific_gravity_min": 3.06,
                "specific_gravity_max": 3.26,
                "size": "5x3x2cm",
                "weight": 58.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=30),
                "price": 3500.0,
                "currency": "CNY",
                "dealer": "阿勒泰宝石专营店",
                "description": "典型的西瓜碧玺，外围绿色，中心粉红色，颜色分界清晰。",
                "notes": "阿勒泰可可托海3号矿坑出产，已打磨成吊坠料。",
                "identification_status": IdentificationStatus.PENDING,
                "owner_id": collector1.id
            },
            {
                "specimen_no": "SP2025010004",
                "name": "烟晶晶簇",
                "mineral_type": "石英",
                "variety": "烟晶",
                "locality": "山东省青岛市崂山",
                "province": "山东省",
                "country": "中国",
                "mohs_hardness_min": 7.0,
                "mohs_hardness_max": 7.0,
                "crystal_system": CrystalSystem.TRIGONAL,
                "crystal_form": "六方柱加菱面体",
                "color": "烟褐色",
                "luster": "玻璃光泽",
                "transparency": "透明至半透明",
                "cleavage": "无",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 2.65,
                "specific_gravity_max": 2.65,
                "size": "15x12x10cm",
                "weight": 1200.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.GIFT,
                "acquisition_date": base_date + timedelta(days=40),
                "price": 0.0,
                "currency": "CNY",
                "dealer": "友人赠送",
                "description": "多晶体共生的烟晶晶簇，颜色均匀，晶体完好无损，部分晶体内含气液包体。",
                "notes": "崂山绿石伴生，天然放射性辐照致色。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector1.id
            },
            {
                "specimen_no": "SP2025010005",
                "name": "蓝铜矿与孔雀石共生",
                "mineral_type": "蓝铜矿",
                "variety": "石青",
                "locality": "湖北省黄石市大冶",
                "province": "湖北省",
                "country": "中国",
                "mohs_hardness_min": 3.5,
                "mohs_hardness_max": 4.0,
                "crystal_system": CrystalSystem.MONOCLINIC,
                "crystal_form": "板状",
                "color": "深蓝色、绿色",
                "luster": "玻璃光泽至土状光泽",
                "transparency": "半透明至不透明",
                "cleavage": "完全",
                "fracture": "贝壳状",
                "streak": "浅蓝色",
                "specific_gravity_min": 3.77,
                "specific_gravity_max": 3.89,
                "size": "10x8x6cm",
                "weight": 450.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=50),
                "price": 880.0,
                "currency": "CNY",
                "dealer": "大冶铜绿山矿物商店",
                "description": "蓝铜矿小晶体与孔雀石共生标本，蓝色与绿色对比鲜明，观赏性强。",
                "notes": "铜矿山氧化带次生矿物，典型标型组合。",
                "identification_status": IdentificationStatus.DISPUTED,
                "owner_id": collector1.id
            },
            {
                "specimen_no": "SP2025010006",
                "name": "雄黄晶体",
                "mineral_type": "雄黄",
                "variety": "鸡冠石",
                "locality": "湖南省娄底市冷水江锡矿山",
                "province": "湖南省",
                "country": "中国",
                "mohs_hardness_min": 1.5,
                "mohs_hardness_max": 2.0,
                "crystal_system": CrystalSystem.MONOCLINIC,
                "crystal_form": "短柱状",
                "color": "橘红色",
                "luster": "树脂光泽至金刚光泽",
                "transparency": "半透明",
                "cleavage": "完全",
                "fracture": "贝壳状",
                "streak": "橙黄色",
                "specific_gravity_min": 3.56,
                "specific_gravity_max": 3.56,
                "size": "6x4x3cm",
                "weight": 85.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=60),
                "price": 2200.0,
                "currency": "CNY",
                "dealer": "锡矿山矿物馆",
                "description": "单晶雄黄，晶体完整，颜色鲜艳，光泽强。",
                "notes": "锡矿山特产，注意避光保存，光照下会转变为雌黄。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector2.id
            },
            {
                "specimen_no": "SP2025010007",
                "name": "辰砂双晶",
                "mineral_type": "辰砂",
                "variety": "朱砂",
                "locality": "贵州省铜仁市万山",
                "province": "贵州省",
                "country": "中国",
                "mohs_hardness_min": 2.0,
                "mohs_hardness_max": 2.5,
                "crystal_system": CrystalSystem.TRIGONAL,
                "crystal_form": "菱面体双晶",
                "color": "朱红色",
                "luster": "金刚光泽",
                "transparency": "半透明",
                "cleavage": "完全",
                "fracture": "贝壳状",
                "streak": "红色",
                "specific_gravity_min": 8.10,
                "specific_gravity_max": 8.20,
                "size": "3x2x1.5cm",
                "weight": 28.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.TRADE,
                "acquisition_date": base_date + timedelta(days=70),
                "price": 1500.0,
                "currency": "CNY",
                "dealer": "与藏友交换",
                "description": "典型的辰砂穿插双晶，晶形完美，光泽强烈。",
                "notes": "万山汞矿经典标本，已闭坑多年，收藏价值高。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector2.id
            },
            {
                "specimen_no": "SP2025010008",
                "name": "方解石双晶",
                "mineral_type": "方解石",
                "variety": "冰洲石",
                "locality": "江西省九江市瑞昌",
                "province": "江西省",
                "country": "中国",
                "mohs_hardness_min": 3.0,
                "mohs_hardness_max": 3.0,
                "crystal_system": CrystalSystem.TRIGONAL,
                "crystal_form": "复三方偏三角面体",
                "color": "无色",
                "luster": "玻璃光泽",
                "transparency": "透明",
                "cleavage": "完全菱面体解理",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 2.71,
                "specific_gravity_max": 2.72,
                "size": "8x6x5cm",
                "weight": 220.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=80),
                "price": 450.0,
                "currency": "CNY",
                "dealer": "瑞昌矿物市场",
                "description": "透明的方解石蝴蝶双晶，双晶面明显，内部纯净。",
                "notes": "具有强双折射现象，可用于光学演示。",
                "identification_status": IdentificationStatus.PENDING,
                "owner_id": collector2.id
            },
            {
                "specimen_no": "SP2025010009",
                "name": "绿色萤石与石英共生",
                "mineral_type": "萤石",
                "variety": "绿色萤石",
                "locality": "内蒙古自治区赤峰市",
                "province": "内蒙古自治区",
                "country": "中国",
                "mohs_hardness_min": 4.0,
                "mohs_hardness_max": 4.0,
                "crystal_system": CrystalSystem.ISOMETRIC,
                "crystal_form": "立方体八面体聚形",
                "color": "浅绿色",
                "luster": "玻璃光泽",
                "transparency": "透明至半透明",
                "cleavage": "完全八面体解理",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 3.18,
                "specific_gravity_max": 3.20,
                "size": "15x12x10cm",
                "weight": 1650.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=90),
                "price": 980.0,
                "currency": "CNY",
                "dealer": "赤峰矿物交易会",
                "description": "大量绿色萤石立方体与乳白色石英共生，萤石晶体最大约1.5cm。",
                "notes": "日光下有轻微荧光效应，适合做陈列标本。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector2.id
            },
            {
                "specimen_no": "SP2025010010",
                "name": "蓝文石",
                "mineral_type": "文石",
                "variety": "蓝文石",
                "locality": "青海省海西蒙古族藏族自治州",
                "province": "青海省",
                "country": "中国",
                "mohs_hardness_min": 3.5,
                "mohs_hardness_max": 4.0,
                "crystal_system": CrystalSystem.ORTHORHOMBIC,
                "crystal_form": "柱状",
                "color": "蓝色",
                "luster": "玻璃光泽",
                "transparency": "半透明",
                "cleavage": "不完全",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 2.94,
                "specific_gravity_max": 2.95,
                "size": "7x5x4cm",
                "weight": 120.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.OTHER,
                "acquisition_date": base_date + timedelta(days=100),
                "price": 3200.0,
                "currency": "CNY",
                "dealer": "网络拍卖",
                "description": "罕见的蓝色文石，颜色均匀，呈放射状集合体。",
                "notes": "含铜致色，为近年新发现的品种。",
                "identification_status": IdentificationStatus.PENDING,
                "owner_id": collector2.id
            },
            {
                "specimen_no": "SP2025010011",
                "name": "托帕石",
                "mineral_type": "黄玉",
                "variety": "托帕石",
                "locality": "云南省文山壮族苗族自治州",
                "province": "云南省",
                "country": "中国",
                "mohs_hardness_min": 8.0,
                "mohs_hardness_max": 8.0,
                "crystal_system": CrystalSystem.ORTHORHOMBIC,
                "crystal_form": "斜方柱",
                "color": "酒黄色",
                "luster": "玻璃光泽",
                "transparency": "透明",
                "cleavage": "完全底面解理",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 3.53,
                "specific_gravity_max": 3.56,
                "size": "4x2x1.5cm",
                "weight": 25.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=110),
                "price": 1800.0,
                "currency": "CNY",
                "dealer": "昆明珠宝城",
                "description": "酒黄色托帕石晶体，晶形完整，透明度高。",
                "notes": "天然色，未经过辐照处理。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector3.id
            },
            {
                "specimen_no": "SP2025010012",
                "name": "海蓝宝单晶",
                "mineral_type": "绿柱石",
                "variety": "海蓝宝石",
                "locality": "新疆维吾尔自治区阿勒泰地区",
                "province": "新疆维吾尔自治区",
                "country": "中国",
                "mohs_hardness_min": 7.5,
                "mohs_hardness_max": 8.0,
                "crystal_system": CrystalSystem.HEXAGONAL,
                "crystal_form": "六方柱",
                "color": "淡蓝色",
                "luster": "玻璃光泽",
                "transparency": "透明",
                "cleavage": "不完全底面解理",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 2.68,
                "specific_gravity_max": 2.78,
                "size": "6x3x2.5cm",
                "weight": 45.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.EXCAVATION,
                "acquisition_date": base_date + timedelta(days=120),
                "price": 2800.0,
                "currency": "CNY",
                "dealer": "可可托海矿务局",
                "description": "六方柱状海蓝宝石晶体，淡蓝色，晶体完整，内部有少量气液包体。",
                "notes": "阿勒泰可可托海3号矿坑出产，含亚铁离子致色。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector3.id
            },
            {
                "specimen_no": "SP2025010013",
                "name": "镁铝榴石",
                "mineral_type": "石榴子石",
                "variety": "镁铝榴石",
                "locality": "江苏省连云港市东海",
                "province": "江苏省",
                "country": "中国",
                "mohs_hardness_min": 6.5,
                "mohs_hardness_max": 7.5,
                "crystal_system": CrystalSystem.ISOMETRIC,
                "crystal_form": "菱形十二面体",
                "color": "深红色",
                "luster": "玻璃光泽至树脂光泽",
                "transparency": "透明至半透明",
                "cleavage": "不明显",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 3.7,
                "specific_gravity_max": 4.2,
                "size": "2.5x2x2cm",
                "weight": 18.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=130),
                "price": 680.0,
                "currency": "CNY",
                "dealer": "东海水晶市场",
                "description": "完美的菱形十二面体镁铝榴石，颜色深红，光泽强。",
                "notes": "产于花岗伟晶岩中，与水晶共生。",
                "identification_status": IdentificationStatus.PENDING,
                "owner_id": collector3.id
            },
            {
                "specimen_no": "SP2025010014",
                "name": "红宝石原矿",
                "mineral_type": "刚玉",
                "variety": "红宝石",
                "locality": "云南省保山市",
                "province": "云南省",
                "country": "中国",
                "mohs_hardness_min": 9.0,
                "mohs_hardness_max": 9.0,
                "crystal_system": CrystalSystem.TRIGONAL,
                "crystal_form": "桶状",
                "color": "玫瑰红色",
                "luster": "玻璃光泽至金刚光泽",
                "transparency": "半透明",
                "cleavage": "不明显",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 3.99,
                "specific_gravity_max": 4.00,
                "size": "3x2x1.8cm",
                "weight": 22.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=140),
                "price": 5600.0,
                "currency": "CNY",
                "dealer": "保山宝玉石公司",
                "description": "红宝石原矿，呈短柱状，表面有典型的生长纹，颜色均匀。",
                "notes": "含铬致色，具有强荧光性，可切磨成宝石。",
                "identification_status": IdentificationStatus.DISPUTED,
                "owner_id": collector3.id
            },
            {
                "specimen_no": "SP2025010015",
                "name": "石膏花",
                "mineral_type": "石膏",
                "variety": "透石膏",
                "locality": "青海省柴达木盆地",
                "province": "青海省",
                "country": "中国",
                "mohs_hardness_min": 2.0,
                "mohs_hardness_max": 2.0,
                "crystal_system": CrystalSystem.MONOCLINIC,
                "crystal_form": "燕尾双晶",
                "color": "无色",
                "luster": "玻璃光泽",
                "transparency": "透明",
                "cleavage": "完全",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 2.32,
                "specific_gravity_max": 2.33,
                "size": "20x15x8cm",
                "weight": 850.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=150),
                "price": 350.0,
                "currency": "CNY",
                "dealer": "盐湖博物馆",
                "description": "大型石膏花，由多组燕尾双晶组成，形态优美。",
                "notes": "盐湖沉积成因，质地较软，需小心保管。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector3.id
            },
            {
                "specimen_no": "SP2025010016",
                "name": "紫水晶晶簇",
                "mineral_type": "石英",
                "variety": "紫水晶",
                "locality": "江苏省连云港市东海",
                "province": "江苏省",
                "country": "中国",
                "mohs_hardness_min": 7.0,
                "mohs_hardness_max": 7.0,
                "crystal_system": CrystalSystem.TRIGONAL,
                "crystal_form": "六方锥",
                "color": "紫色",
                "luster": "玻璃光泽",
                "transparency": "透明至半透明",
                "cleavage": "无",
                "fracture": "贝壳状",
                "streak": "白色",
                "specific_gravity_min": 2.65,
                "specific_gravity_max": 2.65,
                "size": "25x20x15cm",
                "weight": 5200.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=160),
                "price": 2500.0,
                "currency": "CNY",
                "dealer": "东海水晶城",
                "description": "大型紫水晶洞切片，密集生长着紫色水晶晶体，颜色浓郁。",
                "notes": "巴西进口原矿，国内加工。铁离子辐照致色。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector1.id
            },
            {
                "specimen_no": "SP2025010017",
                "name": "锡石单晶",
                "mineral_type": "锡石",
                "variety": "锡石",
                "locality": "云南省红河哈尼族彝族自治州个旧",
                "province": "云南省",
                "country": "中国",
                "mohs_hardness_min": 6.0,
                "mohs_hardness_max": 7.0,
                "crystal_system": CrystalSystem.TETRAGONAL,
                "crystal_form": "四方柱加四方双锥",
                "color": "褐色至黑色",
                "luster": "金刚光泽",
                "transparency": "半透明至不透明",
                "cleavage": "不完全",
                "fracture": "贝壳状",
                "streak": "白黄色",
                "specific_gravity_min": 6.98,
                "specific_gravity_max": 7.02,
                "size": "4x3x2.5cm",
                "weight": 85.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=170),
                "price": 1200.0,
                "currency": "CNY",
                "dealer": "个旧锡矿博物馆",
                "description": "晶形完美的锡石单晶，金刚光泽强烈，晶体完整。",
                "notes": "个旧锡矿经典标本，中国锡都的代表性矿物。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector1.id
            },
            {
                "specimen_no": "SP2025010018",
                "name": "自然铜",
                "mineral_type": "自然铜",
                "variety": "自然铜",
                "locality": "安徽省铜陵市",
                "province": "安徽省",
                "country": "中国",
                "mohs_hardness_min": 2.5,
                "mohs_hardness_max": 3.0,
                "crystal_system": CrystalSystem.ISOMETRIC,
                "crystal_form": "立方体",
                "color": "铜红色",
                "luster": "金属光泽",
                "transparency": "不透明",
                "cleavage": "无",
                "fracture": "锯齿状",
                "streak": "铜红色",
                "specific_gravity_min": 8.9,
                "specific_gravity_max": 8.95,
                "size": "10x8x6cm",
                "weight": 450.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.MINING,
                "acquisition_date": base_date + timedelta(days=175),
                "price": 0.0,
                "currency": "CNY",
                "dealer": "自行采集",
                "description": "自然铜集合体，呈树枝状生长，表面有金属光泽，部分已氧化呈暗褐色。",
                "notes": "铜陵铜官山铜矿采集，产于氧化带。",
                "identification_status": IdentificationStatus.PENDING,
                "owner_id": collector2.id
            },
            {
                "specimen_no": "SP2025010019",
                "name": "辉锑矿",
                "mineral_type": "辉锑矿",
                "variety": "辉锑矿",
                "locality": "湖南省娄底市冷水江锡矿山",
                "province": "湖南省",
                "country": "中国",
                "mohs_hardness_min": 2.0,
                "mohs_hardness_max": 2.5,
                "crystal_system": CrystalSystem.ORTHORHOMBIC,
                "crystal_form": "长柱状",
                "color": "铅灰色",
                "luster": "金属光泽",
                "transparency": "不透明",
                "cleavage": "完全",
                "fracture": "参差状",
                "streak": "铅灰色",
                "specific_gravity_min": 4.63,
                "specific_gravity_max": 4.66,
                "size": "12x8x6cm",
                "weight": 680.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=178),
                "price": 550.0,
                "currency": "CNY",
                "dealer": "锡矿山矿物市场",
                "description": "多根长柱状辉锑矿晶体组成的晶簇，晶面条纹明显。",
                "notes": "世界锑都锡矿山的代表矿物，小心保护解理面。",
                "identification_status": IdentificationStatus.CONFIRMED,
                "owner_id": collector2.id
            },
            {
                "specimen_no": "SP2025010020",
                "name": "祖母绿原石",
                "mineral_type": "绿柱石",
                "variety": "祖母绿",
                "locality": "云南省文山壮族苗族自治州麻栗坡",
                "province": "云南省",
                "country": "中国",
                "mohs_hardness_min": 7.5,
                "mohs_hardness_max": 8.0,
                "crystal_system": CrystalSystem.HEXAGONAL,
                "crystal_form": "六方柱",
                "color": "翠绿色",
                "luster": "玻璃光泽",
                "transparency": "透明至半透明",
                "cleavage": "不完全底面解理",
                "fracture": "贝壳状",
                "streak": "white",
                "specific_gravity_min": 2.72,
                "specific_gravity_max": 2.78,
                "size": "5x2x1.5cm",
                "weight": 28.0,
                "weight_unit": "g",
                "acquisition_method": AcquisitionMethod.PURCHASE,
                "acquisition_date": base_date + timedelta(days=180),
                "price": 12800.0,
                "currency": "CNY",
                "dealer": "麻栗坡祖母绿矿",
                "description": "中国祖母绿原石，六方柱状晶体，颜色鲜艳，内部有典型的气液包体和固相包体。",
                "notes": "麻栗坡猛硐乡出产，含铬和钒致色，被誉为中国祖母绿。",
                "identification_status": IdentificationStatus.PENDING,
                "owner_id": collector3.id
            }
        ]

        for spec_data in specimens_data:
            specimen = Specimen(**spec_data)
            db.add(specimen)

        db.flush()

        print("Creating identification records...")

        identifications_data = [
            {
                "specimen_id": specimens_data[0]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "经显微镜观察和X射线衍射分析，确认为紫色八面体萤石。晶体形态完美，建议作为精品收藏。",
                "suggested_mineral_type": None,
                "confidence": 98,
                "created_at": base_date + timedelta(days=15)
            },
            {
                "specimen_id": specimens_data[1]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "黄铁矿晶形完好，金属光泽强烈，与石英共生关系明确。确认为黄铁矿（愚人金）。",
                "suggested_mineral_type": None,
                "confidence": 99,
                "created_at": base_date + timedelta(days=25)
            },
            {
                "specimen_id": specimens_data[3]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "典型的烟晶晶簇，颜色均匀，透明度好。天然辐照致色，无人工处理迹象。",
                "suggested_mineral_type": None,
                "confidence": 97,
                "created_at": base_date + timedelta(days=45)
            },
            {
                "specimen_id": specimens_data[4]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.DISPUTED,
                "comment": "蓝铜矿特征明显，但伴生的绿色矿物需进一步鉴定是否为孔雀石还是硅孔雀石。建议做红外光谱分析。",
                "suggested_mineral_type": "蓝铜矿(可能含硅孔雀石)",
                "confidence": 65,
                "created_at": base_date + timedelta(days=55)
            },
            {
                "specimen_id": specimens_data[5]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "橘红色、树脂光泽、低硬度，确认为雄黄。注意避光保存以防光化反应。",
                "suggested_mineral_type": None,
                "confidence": 96,
                "created_at": base_date + timedelta(days=65)
            },
            {
                "specimen_id": specimens_data[6]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "辰砂穿插双晶特征典型，朱红色、金刚光泽、大比重，确认为辰砂。已闭坑矿区出产，收藏价值高。",
                "suggested_mineral_type": None,
                "confidence": 99,
                "created_at": base_date + timedelta(days=75)
            },
            {
                "specimen_id": specimens_data[8]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "浅绿色萤石与石英共生组合典型，立方体八面体聚形晶形完好。",
                "suggested_mineral_type": None,
                "confidence": 95,
                "created_at": base_date + timedelta(days=95)
            },
            {
                "specimen_id": specimens_data[10]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "酒黄色托帕石，晶形完整，透明度高。建议做光谱分析确认是否天然色。",
                "suggested_mineral_type": None,
                "confidence": 92,
                "created_at": base_date + timedelta(days=115)
            },
            {
                "specimen_id": specimens_data[11]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "海蓝宝石晶体特征明显，淡蓝色、六方柱状晶形。阿勒泰出产的优质标本。",
                "suggested_mineral_type": None,
                "confidence": 98,
                "created_at": base_date + timedelta(days=125)
            },
            {
                "specimen_id": specimens_data[13]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.DISPUTED,
                "comment": "玫瑰红色刚玉，怀疑颜色经过热处理。建议做宝石检测中心的全面检测以确认是否天然色。",
                "suggested_mineral_type": "刚玉(红宝石，颜色存疑)",
                "confidence": 55,
                "created_at": base_date + timedelta(days=145)
            },
            {
                "specimen_id": specimens_data[14]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "透石膏燕尾双晶集合体，形态优美。盐湖沉积成因，标本完整。",
                "suggested_mineral_type": None,
                "confidence": 99,
                "created_at": base_date + timedelta(days=155)
            },
            {
                "specimen_id": specimens_data[15]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "紫水晶晶簇颜色浓郁，晶体发育良好。紫外线下可见荧光，建议检测是否有辐照处理。",
                "suggested_mineral_type": None,
                "confidence": 94,
                "created_at": base_date + timedelta(days=165)
            },
            {
                "specimen_id": specimens_data[16]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "锡石单晶晶形完美，金刚光泽，比重大。个旧锡矿的代表性标本。",
                "suggested_mineral_type": None,
                "confidence": 97,
                "created_at": base_date + timedelta(days=172)
            },
            {
                "specimen_id": specimens_data[18]["specimen_no"],
                "identifier_id": admin.id,
                "status_before": IdentificationStatus.PENDING,
                "status_after": IdentificationStatus.CONFIRMED,
                "comment": "辉锑矿长柱状晶形，晶面条纹明显，金属光泽强烈。锡矿山经典标本。",
                "suggested_mineral_type": None,
                "confidence": 98,
                "created_at": base_date + timedelta(days=179)
            }
        ]

        specimen_no_to_id = {}
        for spec in db.query(Specimen).all():
            specimen_no_to_id[spec.specimen_no] = spec.id

        for ident_data in identifications_data:
            spec_no = ident_data.pop("specimen_id")
            spec_id = specimen_no_to_id.get(spec_no)
            if spec_id:
                identification = Identification(
                    **ident_data,
                    specimen_id=spec_id
                )
                db.add(identification)

        db.commit()

        print("\n" + "="*60)
        print("Database initialization completed successfully!")
        print("="*60)
        print(f"\nCreated users: {db.query(User).count()}")
        print(f"Created specimens: {db.query(Specimen).count()}")
        print(f"Created identifications: {db.query(Identification).count()}")
        print(f"\nDemo accounts:")
        print(f"  Admin: admin / admin123")
        print(f"  Collector 1: collector1 / 123456")
        print(f"  Collector 2: collector2 / 123456")
        print(f"  Collector 3: collector3 / 123456")
        print("\n" + "="*60)

    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting database initialization...")
    if wait_for_db():
        init_database()
    else:
        print("Database initialization failed")
        sys.exit(1)
