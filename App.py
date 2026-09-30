import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 MÁY TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write("Tính tiền lãi theo phương pháp lãi đơn và lãi kép")


# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ==============================
# NHẬP DỮ LIỆU
# ==============================
st.subheader("📋 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=1000.0,
    value=10_000_000.0,
    step=500_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

loai_lai = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_nhan = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)


# ==============================
# NÚT TÍNH
# ==============================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    # Chuyển lãi suất % sang số thập phân
    r = lai_suat / 100

    # Kỳ hạn tính theo năm
    so_nam = ky_han / 12

    # Xác định số kỳ nhận lãi
    if hinh_thuc_nhan == "Lãnh lãi theo tháng":
        so_ky = ky_han
        thang_moi_ky = 1

    elif hinh_thuc_nhan == "Lãnh lãi theo quý":
        so_ky = ky_han / 3
        thang_moi_ky = 3

    else:
        so_ky = 1
        thang_moi_ky = ky_han

    # Kiểm tra kỳ hạn theo quý
    if hinh_thuc_nhan == "Lãnh lãi theo quý" and ky_han % 3 != 0:
        st.warning(
            "⚠️ Khi chọn lãnh lãi theo quý, kỳ hạn nên là bội số của 3 tháng."
        )

    # ==============================
    # LÃI ĐƠN
    # ==============================
    if loai_lai == "Lãi đơn":

        tong_lai = so_tien * r * so_nam
        tong_tien = so_tien + tong_lai

        # Lãi định kỳ
        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            lai_dinh_ky = so_tien * r / 12

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            lai_dinh_ky = so_tien * r / 4

        else:
            lai_dinh_ky = tong_lai

        # ==============================
        # KẾT QUẢ
        # ==============================
        st.success("✅ Tính toán hoàn tất!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Tiền lãi định kỳ",
                format_money(lai_dinh_ky)
            )

        with col2:
            st.metric(
                "Tổng tiền lãi",
                format_money(tong_lai)
            )

        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_tien)
        )

        # Thông tin chi tiết
        with st.expander("📊 Xem thông tin chi tiết"):
            st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
            st.write(f"**Kỳ hạn:** {ky_han} tháng")
            st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
            st.write(f"**Phương pháp:** {loai_lai}")
            st.write(f"**Nhận lãi:** {hinh_thuc_nhan}")


    # ==============================
    # LÃI KÉP
    # ==============================
    else:

        # Xác định số kỳ ghép lãi
        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            so_ky = ky_han
            lai_suat_ky = r / 12

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            so_ky = ky_han / 3
            lai_suat_ky = r / 4

        else:
            # Cuối kỳ: toàn bộ lãi được nhập vào gốc
            # và tính theo năm
            so_ky = so_nam
            lai_suat_ky = r

        # ==============================
        # Nếu lãnh lãi cuối kỳ
        # ==============================
        if hinh_thuc_nhan == "Lãnh lãi cuối kỳ":

            tong_tien = so_tien * ((1 + r) ** so_nam)
            tong_lai = tong_tien - so_tien
            lai_dinh_ky = tong_lai

        else:

            # Số kỳ phải là số nguyên
            so_ky_int = int(so_ky)

            tong_tien = so_tien * (
                (1 + lai_suat_ky) ** so_ky_int
            )

            tong_lai = tong_tien - so_tien

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = so_tien * lai_suat_ky

        # ==============================
        # KẾT QUẢ
        # ==============================
        st.success("✅ Tính toán hoàn tất!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Tiền lãi định kỳ",
                format_money(lai_dinh_ky)
            )

        with col2:
            st.metric(
                "Tổng tiền lãi",
                format_money(tong_lai)
            )

        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_tien)
        )

        # ==============================
        # BẢNG THÔNG TIN
        # ==============================
        with st.expander("📊 Xem thông tin chi tiết"):

            st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
            st.write(f"**Kỳ hạn:** {ky_han} tháng")
            st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
            st.write(f"**Phương pháp:** {loai_lai}")
            st.write(f"**Nhận lãi:** {hinh_thuc_nhan}")

            if hinh_thuc_nhan == "Lãnh lãi theo tháng":
                st.write("**Chu kỳ ghép lãi:** 1 tháng")

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":
                st.write("**Chu kỳ ghép lãi:** 3 tháng")

            else:
                st.write("**Chu kỳ ghép lãi:** Cuối kỳ")


# ==============================
# GHI CHÚ
# ==============================
st.divider()

st.caption(
    "📌 Lưu ý: Kết quả mang tính chất tham khảo. "
    "Lãi suất thực tế của ngân hàng có thể được tính theo "
    "quy định và phương pháp riêng của từng ngân hàng."
    )
