"""Tests for read-only Interactive HTML Sitemap extraction (`coder-nexus sitemap ...`)."""

from __future__ import annotations

import base64
import json
from pathlib import Path

from coder_nexus.cli import build_parser
from coder_nexus.sitemap import extract_sitemap, inspect_sitemap, is_interactive_sitemap_html
from coder_nexus.sitemap.commands import cmd_sitemap

# Minimal valid 1x1 PNG
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)
TINY_PNG_URI = "data:image/png;base64," + base64.b64encode(TINY_PNG).decode("ascii")


def _build_sample_sitemap_html(leading_prefix: str = "hu") -> str:
    stages = [
        {
            "id": "STAGE_1",
            "code": "TẦNG 1",
            "moduleCode": "M-01 • M-02",
            "title": "KHỞI ĐỘNG & ĐĂNG NHẬP",
            "subtitle": "Auth flow",
        },
        {
            "id": "STAGE_2",
            "code": "TẦNG 2",
            "moduleCode": "M-05 • BS-03",
            "title": "YÊU CẦU BẢO TRÌ",
            "subtitle": "MR management",
        },
    ]
    bridges = [
        {"fromStage": "STAGE_1", "toStage": "STAGE_2", "label": "TẦNG 1 -> TẦNG 2", "type": "horiz"},
    ]
    screens = [
        {
            "id": "H01",
            "num": 1,
            "code": "Hình 01",
            "screenCode": "M-01",
            "group": "M-01",
            "stageId": "STAGE_1",
            "part": "PHẦN 1: KHỞI ĐỘNG",
            "title": "Màn hình Khởi động (`M-01`)",
            "shortTitle": "Khởi động",
            "role": "🏠 Màn hình chính",
            "isMainFlow": True,
            "imgWidth": 2560,
            "imgHeight": 1600,
            "image": TINY_PNG_URI,
            "imageAlt": "Splash",
            "parents": [],
            "children": ["H02"],
            "hotspots": [{"stt": "1", "x1": 100, "y1": 200, "x2": 300, "y2": 260, "label": "Thanh tiến trình"}],
            "htmlContent": (
                '<ul class="overview-list">'
                '<li><strong>Mục đích & Vai trò:</strong> Khởi tạo <code class="inline-code">DI</code>.</li>'
                '<li><strong>Ngữ cảnh xuất hiện (Action Flow):</strong> Route <code class="inline-code">/splash</code>.</li>'
                "</ul>"
                "<table><thead><tr>"
                "<th>STT</th><th>Hình Preview Khu Vực</th><th>Tên Element / Nhãn UI</th>"
                "<th>Chức năng hiển thị & Thao tác người dùng</th><th>Logic Nghiệp vụ / Công thức ngầm</th>"
                "</tr></thead><tbody>"
                "<tr><td>1</td><td>Giữa màn🎯</td><td>Thanh tiến trình Bootstrap</td>"
                "<td>Hiển thị trạng thái tải</td><td>Kiểm tra phiên đăng nhập</td></tr>"
                "</tbody></table>"
            ),
        },
        {
            "id": "H02",
            "num": 2,
            "code": "Hình 02",
            "screenCode": "M-02",
            "group": "M-02",
            "stageId": "STAGE_1",
            "part": "PHẦN 1: KHỞI ĐỘNG",
            "title": "Đăng nhập SSO (`M-02`)",
            "shortTitle": "Đăng nhập",
            "role": "🏠 Màn hình chính",
            "isMainFlow": True,
            "imgWidth": 2560,
            "imgHeight": 1600,
            "image": TINY_PNG_URI,
            "parents": ["H01"],
            "children": ["H03"],
            "hotspots": [
                {"stt": "1", "x1": 400, "y1": 300, "x2": 900, "y2": 360, "label": "Ô nhập Email"},
                {"stt": "2", "x1": 400, "y1": 420, "x2": 900, "y2": 480, "label": "Nút ĐĂNG NHẬP"},
            ],
            "htmlContent": (
                '<ul class="overview-list">'
                '<li><strong>Mục đích & Vai trò:</strong> Đăng nhập tài khoản Portal SSO.</li>'
                "</ul>"
                "<table><thead><tr>"
                "<th>STT</th><th>Hình Preview Khu Vực</th><th>Tên thành phần UI</th>"
                "<th>Chức năng & Tương tác</th><th>Ghi chú / Quy tắc nghiệp vụ</th>"
                "</tr></thead><tbody>"
                "<tr><td>1</td><td>Trường 1🎯</td><td>Ô nhập Email</td><td>Nhập email</td><td>Validate định dạng email</td></tr>"
                "<tr><td>2</td><td>Nút chính🎯</td><td>Nút ĐĂNG NHẬP</td><td>Gửi xác thực</td><td>Tải quyền RBAC hợp nhất</td></tr>"
                "</tbody></table>"
            ),
        },
        {
            "id": "H03",
            "num": 3,
            "code": "Hình 03",
            "screenCode": "M-05",
            "group": "M-05",
            "stageId": "STAGE_2",
            "part": "PHẦN 2: BẢO TRÌ",
            "title": "Danh sách Yêu cầu Bảo trì (`M-05`)",
            "shortTitle": "Danh sách MR",
            "role": "🏠 Màn hình chính",
            "isMainFlow": True,
            "imgWidth": 2560,
            "imgHeight": 1600,
            "image": TINY_PNG_URI,
            "parents": ["H02"],
            "children": ["H04"],
            "hotspots": [{"stt": "1", "x1": 10, "y1": 10, "x2": 500, "y2": 80, "label": "AppBar"}],
            "htmlContent": (
                '<ul class="overview-list"><li><strong>Mục đích:</strong> Theo dõi phiếu MR.</li></ul>'
                "<table><thead><tr><th>STT</th><th>Preview</th><th>Element</th><th>Action</th><th>Logic</th></tr></thead>"
                "<tbody><tr><td>1</td><td>Top🎯</td><td>Tiêu đề AppBar</td><td>Hiển thị đếm SLA</td><td>Highlight quá SLA</td></tr></tbody></table>"
            ),
        },
        {
            "id": "H04",
            "num": 4,
            "code": "Hình 04",
            "screenCode": "BS-03",
            "group": "BS-03",
            "stageId": "STAGE_2",
            "part": "PHẦN 2: BẢO TRÌ",
            "title": "Bộ lọc MR (`BS-03` — Bottom Sheet)",
            "shortTitle": "Bộ lọc MR",
            "role": "💬 Bottom Sheet / Menu",
            "isMainFlow": False,
            "imgWidth": 2560,
            "imgHeight": 1600,
            "image": TINY_PNG_URI,
            "parents": ["H03"],
            "children": [],
            "hotspots": [{"stt": "1", "x1": 10, "y1": 500, "x2": 500, "y2": 560, "label": "Chip Ưu tiên"}],
            "htmlContent": (
                '<ul class="overview-list"><li><strong>Mục đích:</strong> Lọc đa chiều MR.</li></ul>'
                "<table><thead><tr><th>STT</th><th>Preview</th><th>Element</th><th>Action</th><th>Logic</th></tr></thead>"
                "<tbody><tr><td>1</td><td>Giữa🎯</td><td>Nhóm Chip Ưu tiên</td><td>Chọn nhiều mức</td><td>Toán tử IN (...)</td></tr></tbody></table>"
            ),
        },
    ]
    return (
        f"{leading_prefix}<!DOCTYPE html>\n<html><head>"
        "<title>Demo Sitemap v5.0</title></head><body><script>\n"
        f"const STAGES = {json.dumps(stages, ensure_ascii=False)};\n"
        f"const STAGE_BRIDGES = {json.dumps(bridges, ensure_ascii=False)};\n"
        f"const SCREENS = {json.dumps(screens, ensure_ascii=False)};\n"
        "</script></body></html>\n"
    )


def test_detect_and_inspect_sitemap_tolerates_corrupt_doctype_prefix(tmp_path):
    html_file = tmp_path / "sitemap.html"
    html_file.write_text(_build_sample_sitemap_html(leading_prefix="hu"), encoding="utf-8")

    plain_html = tmp_path / "plain.html"
    plain_html.write_text("<html><body><h1>Hello</h1></body></html>", encoding="utf-8")

    assert is_interactive_sitemap_html(html_file) is True
    assert is_interactive_sitemap_html(plain_html) is False
    assert is_interactive_sitemap_html(tmp_path / "missing.html") is False

    res = inspect_sitemap(html_file)
    assert res.status == "READ"
    assert res.title == "Demo Sitemap v5.0"
    assert res.total_stages == 2
    assert res.total_screens == 4
    assert [s["id"] for s in res.stages_summary] == ["STAGE_1", "STAGE_2"]
    assert [s["screen_count"] for s in res.stages_summary] == [2, 2]


def test_extract_sitemap_filters_decodes_png_and_parses_elements(tmp_path):
    html_file = tmp_path / "sitemap.html"
    html_file.write_text(_build_sample_sitemap_html(), encoding="utf-8")
    out_dir = tmp_path / "out"

    # 1) Index-only run writes index files and no screens directory
    idx_res = extract_sitemap(html_file, out_dir, index_only=True)
    assert idx_res.status == "READ"
    assert idx_res.extracted_screens == 0
    assert Path(idx_res.index_md_path).is_file()
    assert Path(idx_res.index_json_path).is_file()
    assert not (out_dir / "screens").exists()

    # 2) Filter by screen code + include neighbors (M-05 -> H03, plus parents H02 and children H04)
    res = extract_sitemap(html_file, out_dir, screen_codes_filter=["M-05"], include_neighbors=True)
    assert res.status == "READ"
    assert res.matched_screens == 3
    assert res.extracted_screens == 3
    assert len(res.screen_images) == 3

    h02_spec = json.loads((out_dir / "screens" / "H02_M-02.spec.json").read_text(encoding="utf-8"))
    assert h02_spec["source_kind"] == "html_sitemap"
    assert h02_spec["viewport"] == {"width": 2560, "height": 1600}
    assert len(h02_spec["elements"]) == 2
    assert h02_spec["elements"][0]["pattern_hint"] == "formfield"
    assert h02_spec["elements"][0]["bbox"] == {"x1": 400, "y1": 300, "x2": 900, "y2": 360}
    assert h02_spec["elements"][1]["pattern_hint"] == "button"
    assert Path(h02_spec["image_path"]).read_bytes() == TINY_PNG

    # 3) Incremental run for H01 preserves previously extracted H02/H03/H04 in index.json
    res_inc = extract_sitemap(html_file, out_dir, ids_filter=["H01-H01"])
    assert res_inc.extracted_screens == 1
    index_data = json.loads((out_dir / "index.json").read_text(encoding="utf-8"))
    assert set(index_data["extracted_screen_ids"]) == {"H01", "H02", "H03", "H04"}


def test_sitemap_cli_inspect_and_extract_creates_sources_gitignore(tmp_path, capsys):
    html_file = tmp_path / "Huong_Dan_Sitemap.html"
    html_file.write_text(_build_sample_sitemap_html(), encoding="utf-8")
    ws = tmp_path / "client_ws"
    ws.mkdir()

    parser = build_parser()

    args_inspect = parser.parse_args(["sitemap", "inspect", str(html_file), "--json"])
    assert cmd_sitemap(args_inspect) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "READ" and payload["total_screens"] == 4

    args_extract = parser.parse_args([
        "sitemap", "extract", str(html_file),
        "--workspace-path", str(ws),
        "--stage", "STAGE_2",
        "--json",
    ])
    assert cmd_sitemap(args_extract) == 0
    ext_payload = json.loads(capsys.readouterr().out)
    assert ext_payload["status"] == "READ"
    assert ext_payload["extracted_screens"] == 2
    assert (ws / ".superpowers" / "sources" / ".gitignore").is_file()
    assert Path(ext_payload["index_md_path"]).is_file()


def test_sitemap_extract_handles_unsupported_and_missing_files(tmp_path):
    bad = tmp_path / "not_a_sitemap.html"
    bad.write_text("<html><body>No screens here</body></html>", encoding="utf-8")

    res_bad = extract_sitemap(bad, tmp_path / "out")
    assert res_bad.status == "UNSUPPORTED"

    res_missing = extract_sitemap(tmp_path / "missing.html", tmp_path / "out")
    assert res_missing.status == "ERROR"
