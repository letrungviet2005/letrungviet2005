# Quản lý GitHub Profile

## Thêm ảnh rồi push

1. Chạy `git pull --ff-only` trước khi bắt đầu chỉnh sửa để lấy commit gallery mới nhất của bot.
2. Bỏ ảnh vào `assets/` hoặc thư mục con, ví dụ `assets/2026/01_Python-workshop.jpg`.
3. Commit và push lên `main`:

   ```sh
   git add assets/
   git commit -m "docs: add new moments"
   git push origin main
   ```

4. Mở tab **Actions → Update profile gallery** và xem lần chạy mới nhất. Khi thành công, bot sẽ tạo commit chỉ sửa README nếu gallery có thay đổi.
5. Trước lần chỉnh sửa tiếp theo, chạy lại `git pull --ff-only`. Nếu local đã có commit khác và pull báo lỗi, cần hòa giải lịch sử bằng rebase/merge rồi mới push; không force-push để bỏ commit của bot.

Không cần nhập danh sách ảnh hoặc sửa README. Xóa/đổi tên ảnh rồi commit/push cũng tự cập nhật. Hỗ trợ JPG, JPEG, PNG, WebP, GIF, không phân biệt chữ hoa/thường. Ảnh phải là file thông thường; không dùng symlink. Script không kiểm tra dữ liệu bên trong ảnh, vì vậy hãy mở ảnh trước khi thêm.

## Tên ảnh và bố cục

- `01_Python-workshop.jpg` → `Python workshop`. Tiền tố số kèm dấu gạch/khoảng trắng được bỏ khỏi caption.
- `02_Buổi học Python.PNG` → `Buổi học Python`. Tên tiếng Việt, khoảng trắng, `&`, `#`, `%` được mã hóa trong URL và escape trong HTML.
- Sắp xếp tự nhiên theo đường dẫn tương đối: `2_...` đứng trước `10_...`. Muốn chọn ảnh nổi bật, đặt các ảnh cùng thư mục và dùng `01_`, `02_`. Tên thư mục cũng ảnh hưởng thứ tự.
- Hai ảnh đầu hiển thị ngay; phần còn lại trong **More moments**. Gallery hai ảnh mỗi hàng, không đặt chiều cao hoặc cắt ảnh. Trên điện thoại, bấm ảnh để đọc bản đầy đủ. Hàng lẻ vẫn hiển thị ảnh còn lại; phần bổ sung cũng chia hai cột.
- Không có ảnh thì toàn bộ tiêu đề và gallery được ẩn.
- `assets/branding/` dành riêng cho banner và trang trí; toàn bộ thư mục bị loại khỏi gallery, kể cả ảnh raster.
- Hai ảnh gốc `award1.png`, `award2.png` được giữ nguyên. Tên chung chung như `award1`, `award2`, `IMG_123`, `photo3` hoặc chỉ có số không hiện caption; alt text dùng mô tả trung tính có số thứ tự. Đổi sang tên có ý nghĩa nếu muốn hiện caption. Không cần metadata hoặc sửa README; script không tự suy diễn tên giải thưởng.

## Thiết lập lần đầu

Commit/push tất cả file bàn giao lên `main`. Nhánh mặc định đã được kiểm tra bằng `git ls-remote --symref origin HEAD`: hiện là `main`. Nếu đổi nhánh mặc định, sửa `on.push.branches` trong workflow cho khớp. Job chỉ chạy trên nhánh mặc định; khi chạy thủ công cũng phải chọn nhánh này.

Repository phải bật GitHub Actions và cho phép hai action chính thức `actions/checkout`, `actions/setup-python`. Job yêu cầu `contents: write` qua `GITHUB_TOKEN` có sẵn; không cần PAT hoặc dịch vụ trả phí. Nếu token bị hạn chế, kiểm tra **Settings → Actions → General → Workflow permissions** và chính sách cấp tổ chức. Chỉ thay đổi quyền nếu bạn có thẩm quyền.

Nếu branch protection/ruleset yêu cầu pull request hoặc chặn bot push trực tiếp, workflow sẽ báo lỗi và không tự thay đổi chính sách. Muốn duy trì cơ chế hoàn toàn tự động, quản trị viên phải cho phép bot cập nhật nhánh theo chính sách của repository. Nếu không được phép, chạy script local và gửi README qua pull request thông thường; đây là phương án cần thao tác thủ công.

Có thể chạy lại tại **Actions → Update profile gallery → Run workflow**. Workflow tuần tự hóa các lần chạy, fetch nhánh mới nhất trước khi tạo gallery, và thử lại tối đa năm lần nếu push bị từ chối. Mỗi lần thử đều tạo lại gallery từ dữ liệu mới; không force-push hoặc rebase nội dung gallery cũ. Reset chỉ diễn ra trong checkout tạm trên runner. Commit chỉ thay README không khớp bộ lọc đường dẫn nên không tạo vòng lặp.

## Chạy và kiểm tra local

Cần Python 3.10 trở lên, chỉ dùng thư viện chuẩn:

```sh
python scripts/update_gallery.py
python -B -m unittest discover -s scripts -p "test_*.py" -v
```

Có thể gọi script từ thư mục khác: mặc định script tìm root từ chính vị trí của nó. `--root` dành cho một bản sao repository khi kiểm thử.

Không xóa/nhân đôi hai marker `<!-- GALLERY:START -->` và `<!-- GALLERY:END -->`. Script chỉ thay byte nằm giữa chúng, giữ nguyên mọi nội dung ngoài marker, không chèn thời gian. Thiếu, trùng hoặc đảo marker đều gây lỗi trước khi ghi. Không chỉnh tay bên trong vùng sinh tự động vì lần chạy sau sẽ thay thế nội dung đó.

Các bài kiểm thử dùng thư mục tạm tự dọn dẹp, bao gồm gallery rỗng, thêm/xóa/đổi tên, Unicode/ký tự đặc biệt, thứ tự, phần thu gọn, loại branding, chạy lặp, bảo toàn byte ngoài marker và marker lỗi.

## Điều kiện hiển thị trên profile

Repository công khai phải mang đúng tên username: `letrungviet2005/letrungviet2005`. File `README.md` phải nằm ở root của nhánh mặc định và có nội dung. Xem profile sau khi push để kiểm tra render thật; bản preview local không xác nhận GitHub Actions hoặc bộ lọc HTML của GitHub đã chạy.

Banner dùng `<picture>`: bản mobile riêng ở viewport tối đa 600px, bản desktop 1200 × 360 cho light/dark. Cả hai giao diện giữ bảng màu Midnight Developer Studio. SVG tự chứa, dùng font hệ thống, không JavaScript. Các ô BUILD / TEACH / EXPLORE và thẻ dự án là ảnh riêng, tự xuống dòng theo chiều rộng. Nội dung giới thiệu và dự án vẫn có dạng chữ và liên kết trong README. Icon và badge đã lưu local; nguồn nằm trong [BRANDING_SOURCES.md](BRANDING_SOURCES.md).

## Nguồn xác minh và lựa chọn nội dung

Kiểm tra ngày 01/11/2026:

- [GoPitch Backend README](https://github.com/letrungviet2005/GoPitch-BE/blob/main/README.md) mô tả API đặt sân; [pom.xml](https://github.com/letrungviet2005/GoPitch-BE/blob/main/pom.xml) xác nhận Java, Spring Boot và MySQL.
- [Fall Detection main.py](https://github.com/letrungviet2005/Fall-detection/blob/main/main.py) xác nhận phân tích video, pose, chuyển động và các import OpenCV/NumPy. Không khẳng định hiệu quả hoặc mức độ sẵn sàng triển khai của dự án.
- Endpoint stats cũ `https://github-readme-stats.vercel.app/api?username=letrungviet2005&show_icons=true&theme=tokyonight&hide_border=true` trả HTTP 503, nên đã bỏ stats và top-languages phụ thuộc cùng dịch vụ.
- Endpoint streak trong README trả HTTP 200 với SVG chứa dữ liệu đóng góp, nên giữ duy nhất widget này. Đây là dịch vụ ngoài và có thể lỗi về sau; liên kết GitHub bằng chữ vẫn dùng được. Contribution graph được bỏ để giữ bố cục gọn.
- Phiên bản chính thức đã kiểm tra: [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1), [setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0). Workflow cố định phiên bản cụ thể; kiểm tra release chính thức trước khi nâng cấp.

## Kiểm chứng lần nâng cấp Midnight Developer Studio — 01/11/2026

- Local: 8/8 bài kiểm thử gallery đạt; chạy script lần hai báo `Gallery already up to date`. Kiểm tra thêm caption chung chung, hàng hai ảnh, hàng lẻ, liên kết ảnh gốc; các kiểm thử cũ về loại branding, Unicode và bảo toàn nội dung ngoài marker vẫn đạt.
- Tất cả 17 SVG trong `assets/branding/` đã được nhúng trong README và parse XML thành công. Mọi đường dẫn ảnh local tồn tại. Gallery thực tế chỉ gồm `assets/award1.png` và `assets/award2.png`; không có tài nguyên branding.
- HTML README được tạo bằng GitHub Markdown API, sau đó render local bằng Edge headless với github-markdown-css 5.8.1. Đã xem ảnh chụp light/dark ở 390px và 1100px: không ảnh lỗi, không tràn ngang; mobile chọn đúng banner riêng, thẻ tự xuống dòng, gallery không bị cắt hoặc kéo giãn. CSS chỉ dùng trong preview, không nhúng vào README.
- Kiểm tra mạng: các endpoint icon/badge trả HTTP 200, nội dung SVG hợp lệ trước khi lưu local. Widget streak dùng đúng `user=letrungviet2005`, HTTP 200, SVG có dữ liệu đóng góp và các nhãn thống kê; nhúng bằng `<img>` với palette navy/cyan/indigo, không dùng camo hay ảnh thống kê giả. Dữ liệu thuộc dịch vụ ngoài, có thể thay đổi hoặc ngừng tải về sau; liên kết activity bằng chữ vẫn có sẵn.
- Nguồn dự án được đọc lại từ GitHub: GoPitch README (UTF-16LE) và pom.xml; Fall Detection main.py. Chỉ mô tả chức năng và công nghệ có trong các nguồn này.

Chưa commit/push thay đổi, chưa kiểm tra profile đã xuất bản hoặc chạy workflow trên GitHub trong lần nâng cấp này. Kiểm tra API Markdown không tương đương kiểm tra trang profile thực tế, quyền ghi bot hoặc branch protection. Workflow hiện có được giữ nguyên.
