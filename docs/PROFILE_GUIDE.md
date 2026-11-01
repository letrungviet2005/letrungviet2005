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
- Hai ảnh đầu hiển thị ngay; phần còn lại trong **More moments**. Gallery một cột để ảnh chứng nhận dễ xem trên màn hình nhỏ, không đặt chiều cao hoặc cắt ảnh. Bấm ảnh để mở bản đầy đủ.
- Không có ảnh thì toàn bộ tiêu đề và gallery được ẩn.
- `assets/branding/` dành riêng cho banner và trang trí; toàn bộ thư mục bị loại khỏi gallery, kể cả ảnh raster.
- Hai ảnh gốc `award1.png`, `award2.png` được giữ nguyên. Caption hiện là tên file; hãy đổi sang tên mô tả chính xác nếu muốn đẹp hơn. Script không tự suy diễn tên giải thưởng.

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

Banner SVG sáng/tối dùng `<picture>` theo giao diện người xem, không tải font bên ngoài hoặc JavaScript. Nội dung quan trọng vẫn có dạng chữ trong README.

## Nguồn xác minh và lựa chọn nội dung

Kiểm tra ngày 01/11/2026:

- [GoPitch Backend README](https://github.com/letrungviet2005/GoPitch-BE/blob/main/README.md) mô tả API đặt sân; [pom.xml](https://github.com/letrungviet2005/GoPitch-BE/blob/main/pom.xml) xác nhận Java, Spring Boot và MySQL.
- [Fall Detection main.py](https://github.com/letrungviet2005/Fall-detection/blob/main/main.py) xác nhận phân tích video, pose, chuyển động và các import OpenCV/NumPy. Không khẳng định hiệu quả hoặc mức độ sẵn sàng triển khai của dự án.
- Endpoint stats cũ `https://github-readme-stats.vercel.app/api?username=letrungviet2005&show_icons=true&theme=tokyonight&hide_border=true` trả HTTP 503, nên đã bỏ stats và top-languages phụ thuộc cùng dịch vụ.
- Endpoint streak trong README trả HTTP 200 với SVG chứa dữ liệu đóng góp, nên giữ duy nhất widget này. Đây là dịch vụ ngoài và có thể lỗi về sau; liên kết GitHub bằng chữ vẫn dùng được. Contribution graph được bỏ để giữ bố cục gọn.
- Phiên bản chính thức đã kiểm tra: [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1), [setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0). Workflow cố định phiên bản cụ thể; kiểm tra release chính thức trước khi nâng cấp.

Đã kiểm tra local: 7 bài kiểm thử đạt; chạy script hai lần cho kết quả ổn định; YAML và actionlint v1.7.12 không báo lỗi; SVG hợp lệ và đường dẫn ảnh tồn tại. README đã được chuyển sang HTML bằng GitHub Markdown API rồi xem trong Edge headless với CSS mô phỏng GitHub: sáng/tối, desktop 1100px và mobile 390px, không tràn ngang, cả hai ảnh gốc tải được. Đã tắt animation của streak và kiểm tra SVG cuối có nội dung đầy đủ. Preview là kiểm tra bố cục local, không phải ảnh chụp profile đã xuất bản.

Workflow chưa được chạy trên GitHub trong lần bàn giao này. Kết quả local không xác nhận quyền ghi của bot hoặc branch protection. Không có thao tác commit/push tự động từ máy của bạn trong lần triển khai này.
