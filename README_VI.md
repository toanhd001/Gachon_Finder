# 🏫 Gachon Campus Path & Resource Finder Pro

Dự án cuối kỳ môn Cấu trúc dữ liệu và Giải thuật (2026) trường Đại học Gachon. Hệ thống được xây dựng hoàn toàn bằng **Python** kết hợp giao diện Web **Streamlit UI**, phân tách kiến trúc dạng mô-đun độc lập cho 3 thành viên.

[👉 Read the English version here](./README.md)

---

## 🚀 1. Hướng dẫn khởi động nhanh (Dành cho thành viên)

Yêu cầu làm đúng theo các bước sau để chạy dự án trên máy cá nhân:

### Điều kiện tiên quyết

Máy tính đã cài đặt Python 3 (Khuyến khích bản mới nhất).

### Các lệnh cài đặt & Khởi chạy

```bash
# Bước 1: Clone dự án về máy
git clone <URL_REPOSITORY_CỦA_BẠN>
cd Gachon_Finder

# Bước 2: Tạo môi trường ảo (Bắt buộc để tránh lỗi hệ thống trên Mac/Linux)
python3 -m venv .venv

# Bước 3: Kích hoạt môi trường ảo
# Trên macOS/Linux:
source .venv/bin/activate
# Trên Windows (Command Prompt):
# .venv\Scripts\activate.bat

# Bước 4: Cài đặt các thư viện bổ trợ
pip install -r requirements.txt

# Bước 5: Khởi chạy giao diện Web
streamlit run main.py
```

---

## 🌿 2. Quy chuẩn chia Nhánh (Branch) & Commit Code

### Chiến lược phân nhánh

Tuyệt đối không push code trực tiếp lên `main`. Mỗi người tự chịu trách nhiệm trên nhánh riêng:

- Member 1: `feat/member1-navigation`
- Member 2: `feat/member2-booking`
- Member 3: `feat/member3-traffic`

### Quy trình làm việc hàng ngày tránh xung đột (Conflict)

```bash
# 1. Cập nhật code mới nhất từ nhóm về máy
git checkout main
git pull origin main

# 2. Chuyển sang nhánh tính năng của mình để làm việc
git checkout -b feat/memberX-ten-tinh-nang

# 3. Tiến hành Code và chạy thử bằng Streamlit. Khi code đã chạy mượt, tiến hành lưu:
git add .
git commit -m "feat: mô tả ngắn gọn tính năng vừa thêm"

# 4. Đẩy nhánh lên GitHub
git push origin feat/memberX-ten-tinh-nang

# 5. Lên giao diện GitHub, tạo Pull Request (PR) để Trưởng nhóm duyệt và Merge.
```

### Quy ước đặt tên Commit (Commit Message Standards)

Bắt buộc dùng các tiền tố quy chuẩn sau để phân loại lịch sử code:

- `feat:` Khi thêm tính năng mới hoặc nâng cấp UI (Ví dụ: `feat: add bar chart for member 3`)
- `fix:` Khi sửa lỗi code (Ví dụ: `fix: fix binary search out of bounds error`)
- `docs:` Khi chỉ sửa đổi tài liệu, comment, hướng dẫn (Ví dụ: `docs: update readme code lines`)

---

## 👥 3. Phân chia chức năng và Nhiệm vụ

Để đạt điểm tối đa ở tiêu chí **"Mức độ hoàn thiện sản phẩm"**, mỗi thành viên quản lý file thuật toán của mình và có nhiệm vụ nâng cấp "Làm đẹp" giao diện Tab tương ứng trên Web:

| Thành viên | File Module phụ trách | Cấu trúc dữ liệu & Giải thuật lõi | Nhiệm vụ làm đẹp giao diện UI (Streamlit) |
| --- | --- | --- | --- |
| **Member 1** | `modules/navigation.py` | Graph Topology, Dijkstra, A* Search | Hiển thị sơ đồ mạng lưới bằng GraphViz, tự động tô đỏ tuyến đường ngắn nhất. |
| **Member 2** | `modules/booking.py` | Chaining Hash Table, BST, Quick Sort, Binary Search | Hiển thị bảng dữ liệu phòng học trực quan, thêm thanh trượt (Slider) lọc phòng theo sức chứa. |
| **Member 3** | `modules/traffic.py` | Priority Queue (Max-Heap), Heap Sort, Kruskal's MST | Vẽ biểu đồ cột (Bar Chart/Plotly) thống kê trực quan mức độ nguy hiểm của các sự cố giao thông. |

---

> **Lưu ý quan trọng:** Nếu bất kỳ thành viên nào cài thêm một thư viện ngoài bằng lệnh pip, bắt buộc phải chạy lệnh `pip freeze > requirements.txt` trước khi commit code để cập nhật danh sách thư viện cho cả nhóm.
