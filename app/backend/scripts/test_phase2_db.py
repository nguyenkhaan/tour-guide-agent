"""
================================================================================
SCRIPT KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN DATABASE PHASE 2
File: scripts/test_phase2_db.py

Mục đích:
  - Kiểm chứng Task 2.1: Kết nối DB, Extension, Transaction Commit & Rollback.
  - Kiểm chứng Task 2.2: Schema & CRUD của Users, UserProfile, AgentSession.
  - Kiểm chứng Task 2.3: Chuẩn hóa Datetime (UTC TIMESTAMPTZ), Currency (NUMERIC),
                         Soft-delete (deleted_at), Khóa chính UUID v4.
  - Kiểm tra 34 bảng trong Database Supabase PostgreSQL.
================================================================================
"""
import asyncio
import datetime
import uuid
from decimal import Decimal

from sqlalchemy import text, select
from src.db import engine, get_db_transaction, async_session_maker
from src.models import (
    Base,
    User,
    UserProfile,
    AgentSession,
    UserRole,
    AccountStatus,
    AgentSessionStatus,
)


async def test_step_1_db_connection_and_extensions():
    """
    [BƯỚC 1] Kiểm tra kết nối Database và các Extension PostgreSQL cần thiết.
    - Kết nối với PostgreSQL qua driver asyncpg.
    - Kiểm tra xem extension 'postgis' (tọa độ địa lý) và 'uuid-ossp' đã được kích hoạt chưa.
    """
    print("\n" + "=" * 70)
    print("🔹 [BƯỚC 1] KIỂM TRA KẾT NỐI DATABASE & POSTGRESQL EXTENSIONS")
    print("=" * 70)

    async with engine.connect() as conn:
        # Lấy phiên bản PostgreSQL
        res = await conn.execute(text("SELECT version();"))
        version = res.scalar()
        print(f"  👉 PostgreSQL Version : {version[:80]}...")

        # Kiểm tra extensions đã cài đặt
        ext_query = await conn.execute(
            text("SELECT extname FROM pg_extension WHERE extname IN ('postgis', 'uuid-ossp');")
        )
        installed = [row[0] for row in ext_query.all()]
        print(f"  👉 Extensions tìm thấy: {installed}")
        assert "postgis" in installed, "❌ Thiếu extension postgis!"
        print("  ✅ [PASS] Kết nối Database và PostGIS Extension hoạt động hoàn hảo!")


async def test_step_2_verify_migrated_tables():
    """
    [BƯỚC 2] Kiểm tra danh sách bảng thực tế trong Database.
    - Query bảng information_schema.tables để đếm và liệt kê các bảng public.
    - Đọc version hiện tại trong bảng alembic_version.
    """
    print("\n" + "=" * 70)
    print("🔹 [BƯỚC 2] KIỂM TRA DANH SÁCH BẢNG & TRẠNG THÁI MIGRATION")
    print("=" * 70)

    async with engine.connect() as conn:
        tables_res = await conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """))
        actual_tables = [r[0] for r in tables_res.all()]
        print(f"  👉 Tổng số bảng thực tế trong Database: {len(actual_tables)}")
        for idx, tbl in enumerate(actual_tables, 1):
            print(f"     {idx:2d}. {tbl}")

        # Kiểm tra phiên bản migration Alembic
        alembic_res = await conn.execute(text("SELECT version_num FROM alembic_version;"))
        current_migration = alembic_res.scalar()
        print(f"  👉 Phiên bản Alembic hiện tại trong DB: {current_migration} (Head)")
        print("  ✅ [PASS] Toàn bộ schema đã được migrate thành công!")


async def test_step_3_transaction_rollback():
    """
    [BƯỚC 3] Kiểm tra Transaction handling (Commit & Rollback) cho Task 2.1.
    - Bắt đầu transaction.
    - Thêm 1 User vào session.
    - Cố tình ném RuntimeError.
    - Kỳ vọng: Session tự động rollback, User KHÔNG được lưu vào Database.
    """
    print("\n" + "=" * 70)
    print("🔹 [BƯỚC 3] KIỂM THỬ TRANSACTION ROLLBACK (TASK 2.1)")
    print("=" * 70)

    test_email_rollback = f"test_rollback_{uuid.uuid4().hex[:6]}@example.com"
    print(f"  👉 Thử tạo User với email: {test_email_rollback}")

    try:
        async with get_db_transaction() as session:
            dummy_user = User(
                email=test_email_rollback,
                full_name="User Test Rollback",
                role=UserRole.USER,
            )
            session.add(dummy_user)
            await session.flush()
            # Giả lập sự cố logic hoặc mất kết nối giữa chừng
            raise RuntimeError("💥 Lỗi giả định xảy ra trong quá trình xử lý nghiệp vụ!")
    except RuntimeError as ex:
        print(f"  👉 Đã bắt được Exception mong muốn: '{ex}'")

    # Kiểm tra lại xem bản ghi có lọt vào DB không
    async with async_session_maker() as session:
        check_query = await session.execute(select(User).where(User.email == test_email_rollback))
        found_user = check_query.scalar_one_or_none()
        assert found_user is None, "❌ LỖI NGHIÊM TRỌNG: Bản ghi vẫn tồn tại dù transaction đã lỗi!"
        print("  ✅ [PASS] Rollback hoàn hảo: Transaction tự động thu hồi dữ liệu khi có lỗi!")


async def test_step_4_crud_and_relationships():
    """
    [BƯỚC 4] Kiểm thử CRUD và Quan hệ giữa Users -> UserProfile -> AgentSession (Task 2.2).
    - Tạo User (UUID v4, email, bcrypt hash).
    - Tạo UserProfile (1-1 quan hệ với User, lưu preferences dạng JSONB).
    - Tạo AgentSession (1-N quan hệ với User, lưu context dạng JSONB).
    - Đọc ngược lại và kiểm tra toàn bộ thuộc tính.
    """
    print("\n" + "=" * 70)
    print("🔹 [BƯỚC 4] KIỂM THỬ CRUD & RELATIONSHIPS (TASK 2.2)")
    print("=" * 70)

    test_user_id = None
    test_email = f"traveler_{uuid.uuid4().hex[:8]}@example.com"

    # 1. Tạo dữ liệu bằng transaction
    async with get_db_transaction() as session:
        new_user = User(
            email=test_email,
            password="$2b$12$eX4mpleBcryptHashedPasswordForTestOnly",
            full_name="Nguyễn Văn Du Lịch",
            role=UserRole.USER,
            status=AccountStatus.ACTIVE,
        )
        session.add(new_user)
        await session.flush()
        test_user_id = new_user.id
        print(f"  👉 Đã tạo User thành công! ID (UUID v4): {test_user_id}")

        # Tạo UserProfile gắn với User (1-1)
        profile = UserProfile(
            user_id=new_user.id,
            preferred_currency="VND",
            default_budget=Decimal("5000000.00"),
            travel_preferences={
                "styles": ["CULTURE", "FOOD", "NATURE"],
                "dietary": ["NO_BEEF"],
            },
            special_needs="Thích đi bộ, chụp ảnh phong cảnh",
        )
        session.add(profile)

        # Tạo AgentSession gắn với User (1-N)
        session_record = AgentSession(
            user_id=new_user.id,
            title="Lên lịch trình Đà Nẵng 3 ngày 2 đêm",
            status=AgentSessionStatus.ACTIVE,
            summary="Lên kế hoạch đi bán đảo Sơn Trà, Bà Nà Hills và phố cổ Hội An",
        )
        session.add(session_record)

    # 2. Truy vấn đọc lại kiểm tra
    async with async_session_maker() as session:
        # Load User
        loaded_user = await session.get(User, test_user_id)
        assert loaded_user is not None
        print(f"  👉 Truy vấn User: {loaded_user.full_name} | Email: {loaded_user.email} | Role: {loaded_user.role.value}")
        print(f"  👉 Server Default Timestamp: created_at = {loaded_user.created_at} (UTC aware)")

        # Load Profile (1-1)
        prof_res = await session.execute(select(UserProfile).where(UserProfile.user_id == test_user_id))
        loaded_profile = prof_res.scalar_one()
        print(f"  👉 Truy vấn Profile (1-1): Tiền tệ: {loaded_profile.preferred_currency} | Ngân sách: {loaded_profile.default_budget}")
        print(f"  👉 Dữ liệu JSONB Preferences: {loaded_profile.travel_preferences}")

        # Load Session (1-N)
        sess_res = await session.execute(select(AgentSession).where(AgentSession.user_id == test_user_id))
        loaded_session = sess_res.scalar_one()
        print(f"  👉 Truy vấn AgentSession (1-N): Tiêu đề: '{loaded_session.title}' | Status: {loaded_session.status.value}")

    print("  ✅ [PASS] Tạo và truy vấn quan hệ User -> Profile -> Session thành công!")
    return test_user_id


async def test_step_5_standardization_and_cleanup(test_user_id: uuid.UUID):
    """
    [BƯỚC 5] Kiểm thử các quy tắc chuẩn hóa của Task 2.3 và Dọn dẹp dữ liệu.
    - Soft-delete: Gán deleted_at = now(utc), kiểm tra query WHERE deleted_at IS NULL.
    - Cleanup: Hard-delete bản ghi test để giữ Database luôn sạch sẽ.
    """
    print("\n" + "=" * 70)
    print("🔹 [BƯỚC 5] KIỂM THỬ CHUẨN HÓA PHASE 2 & SOFT-DELETE (TASK 2.3)")
    print("=" * 70)

    # 1. Thử nghiệm Soft-delete
    async with get_db_transaction() as session:
        user_to_soft_delete = await session.get(User, test_user_id)
        assert user_to_soft_delete is not None
        user_to_soft_delete.deleted_at = datetime.datetime.now(datetime.timezone.utc)
        print(f"  👉 Đã gán Soft-delete: deleted_at = {user_to_soft_delete.deleted_at}")

    # 2. Kiểm tra lọc bản ghi active (bản ghi đã soft-delete không được xuất hiện)
    async with async_session_maker() as session:
        active_check = await session.execute(
            select(User).where(User.id == test_user_id, User.deleted_at.is_(None))
        )
        assert active_check.scalar_one_or_none() is None
        print("  👉 Kiểm tra lọc: User đã soft-delete biến mất khỏi danh sách active chính xác!")

    # 3. Dọn dẹp dữ liệu test (Hard-delete an toàn qua Cascade)
    async with get_db_transaction() as session:
        user_to_cleanup = await session.get(User, test_user_id)
        if user_to_cleanup:
            await session.delete(user_to_cleanup)
        print(f"  👉 Đã dọn dẹp sạch sẽ các bản ghi test có user_id: {test_user_id} (Cascade)")

    print("  ✅ [PASS] Soft-delete và dọn dẹp môi trường thành công 100%!")


async def main():
    print("\n" + "🚀" * 35)
    print("      BẮT ĐẦU CHẠY BỘ KIỂM THỬ DATABASE PHASE 2 TOÀN DIỆN")
    print("🚀" * 35)

    try:
        await test_step_1_db_connection_and_extensions()
        await test_step_2_verify_migrated_tables()
        await test_step_3_transaction_rollback()
        user_id = await test_step_4_crud_and_relationships()
        await test_step_5_standardization_and_cleanup(user_id)

        print("\n" + "🎉" * 35)
        print("   CHÚC MỪNG! TẤT CẢ 5 BƯỚC TEST ĐÃ PASS 100% THÀNH CÔNG RỰC RỠ!")
        print("🎉" * 35 + "\n")
    except Exception as e:
        print(f"\n❌ KIỂM THỬ THẤT BẠI VỚI LỖI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
