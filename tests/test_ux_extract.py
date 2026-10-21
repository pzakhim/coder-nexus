"""Design-source detection and HTML kit generation (`coder-nexus ux extract|viewports`)."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from coder_nexus.ux.kitgen import extract, load_viewports, save_viewports
from coder_nexus.ux.source import resolve_design_system


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def make_kit(root: Path) -> Path:
    write(root / "pubspec.yaml", """name: app_ui_kit
flutter:
  fonts:
  - family: Jakarta
    fonts:
      - asset: lib/assets/fonts/Jakarta-Bold.ttf
        weight: 700
      - asset: lib/assets/fonts/Jakarta-Regular.ttf
        style: normal
""")
    (root / "lib/assets/fonts").mkdir(parents=True)
    (root / "lib/assets/fonts/Jakarta-Bold.ttf").write_bytes(b"ttf")
    (root / "lib/assets/fonts/Jakarta-Regular.ttf").write_bytes(b"ttf")
    write(root / "lib/app_ui_kit/app_color.dart", """class AppColor {
  static const primary = Color(0xFF4B7ABD);
  static const primaryLight = Color(0xFF66B3FF);
  static const white = Color(0xFFFFFFFF);
  static const textPrimary = Color(0xFF111827);
  static const textOnPrimary = white;
  static const error = Color(0xFFFC5656);
  static const info = primary;
  static const shadowColor = Color(0x1A000000);
}""")
    write(root / "lib/app_ui_kit/app_button.dart", """class AppButton extends StatelessWidget {
  AppButton({this.height = 52});
  build() => RoundedRectangleBorder(borderRadius: borderRadius ?? BorderRadius.circular(10));
}
class AppBackButton extends StatelessWidget {}""")
    write(root / "lib/app_ui_kit/app_formfield.dart", """class AppFormField extends StatefulWidget {}
x = OutlineInputBorder(borderRadius: BorderRadius.circular(6));
contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),""")
    write(root / "lib/app_ui_kit/shimmers.dart", "class UnitHeaderCellShimmer extends StatelessWidget {}\nclass BlockSelectorShimmer extends StatelessWidget {}")
    write(root / "lib/app_ui_kit/special.dart", "class AppSpecialNavItem extends StatefulWidget {}")
    return root


def test_app_ui_kit_source_tokens_geometry_and_components(tmp_path):
    kit = make_kit(tmp_path / "app-ui-kit")
    system = resolve_design_system(kit)
    assert system["source"]["kind"] == "app-ui-kit" and system["source"]["profile_hint"] == "imespro"
    assert system["roles"]["primary"] == {"value": "#4b7abd", "from": "AppColor.primary"}
    assert system["roles"]["on-primary"]["value"] == "#ffffff"  # alias textOnPrimary = white
    assert system["roles"]["shadow"]["value"].startswith("rgba(0, 0, 0, 0.1")
    assert system["roles"]["border"]["from"] == "material3 default"
    assert system["geometry"]["button-height"] == "52px" and system["geometry"]["radius-button"] == "10px"
    assert system["geometry"]["radius-input"] == "6px" and system["geometry"]["input-padding"] == "10px 14px"
    assert system["font"]["family"] == "Jakarta" and len(system["font"]["files"]) == 2
    comps = {c["widget"]: c["kit_class"] for c in system["components"]}
    assert comps["UnitHeaderCellShimmer"] == "app-shimmer" and comps["BlockSelectorShimmer"] == "app-shimmer"
    assert comps["AppBackButton"] == "app-appbar" and comps["AppSpecialNavItem"] is None


def test_client_using_kit_through_sibling_path(tmp_path):
    make_kit(tmp_path / "app-ui-kit")
    app = tmp_path / "wms-app"
    write(app / "pubspec.yaml", "name: wms\ndependencies:\n  app_ui_kit:\n    path: ../app-ui-kit\n")
    write(app / "lib/main.dart", "void main() {}")
    system = extract(app)
    assert system["source"]["kind"] == "app-ui-kit"
    kit_dir = app / ".superpowers/ux/kit"
    css = (kit_dir / "kit.css").read_text()
    assert "--c-primary: #4b7abd; /* AppColor.primary */" in css and '--font: "Jakarta"' in css
    assert "@font-face" in css and (kit_dir / "fonts/Jakarta-Bold.ttf").exists()
    for name in ("kit.js", "viewports.js", "components.html", "README.md"):
        assert (kit_dir / name).exists(), name
    assert ".app-button" in (kit_dir / "components.html").read_text()


def test_client_theme_without_kit(tmp_path):
    app = tmp_path / "shop"
    write(app / "pubspec.yaml", "name: shop\n")
    write(app / "lib/core/theme/app_colors.dart", """class AppColors {
  static const brand = Color(0xFF0E7C66);
  static const textColor = Color(0xFF222222);
  static const textSecondary = Color(0xFF666666);
  static const border = Color(0xFFDDDDDD);
  static const danger = Color(0xFFD32F2F);
  static const success = Color(0xFF2E7D32);
  static const background = Color(0xFFFAFAFA);
}""")
    write(app / "lib/shared/widgets/primary_button.dart", "class PrimaryButton extends StatelessWidget {}")
    write(app / "lib/shared/widgets/rating_stars.dart", "class RatingStars extends StatelessWidget {}")
    system = resolve_design_system(app)
    assert system["source"]["kind"] == "client-theme" and system["source"]["profile_hint"] == "external-structured"
    roles = system["roles"]
    assert roles["primary"] == {"value": "#0e7c66", "from": "client.brand"}
    assert roles["error"]["from"] == "client.danger" and roles["text"]["from"] == "client.textColor"
    comps = {c["widget"]: c for c in system["components"]}
    assert comps["PrimaryButton"]["kit_class"] == "app-button" and comps["PrimaryButton"]["status"] == "client"
    assert comps["RatingStars"]["status"] == "code-only"


def test_plain_flutter_uses_material3_with_seed(tmp_path):
    app = tmp_path / "plain"
    write(app / "pubspec.yaml", "name: plain\n")
    write(app / "lib/main.dart", "final t = ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0055AA)));")
    system = resolve_design_system(app)
    assert system["source"]["kind"] == "material3"
    assert system["roles"]["primary"] == {"value": "#0055aa", "from": "theme seed color"}
    assert system["font"]["family"] == "Roboto" and not system["warnings"]
    assert {c["status"] for c in system["components"]} == {"framework"}


def test_nothing_found_asks_user_and_overrides_are_kept(tmp_path):
    app = tmp_path / "blank"
    write(app / "pubspec.yaml", "name: blank\n")
    system = extract(app)
    assert any("ask the user" in w for w in system["warnings"])
    # user answers: brand + font, and the source decision is recorded
    system = extract(app, brand="#aa3300", font="Inter")
    path = app / ".superpowers/ux/design-system.json"
    data = json.loads(path.read_text())
    data["source"]["decision"] = "D-03"
    path.write_text(json.dumps(data))
    again = extract(app)  # re-run keeps overrides and the decision
    assert again["roles"]["primary"] == {"value": "#aa3300", "from": "user override"}
    assert again["font"]["family"] == "Inter" and again["source"]["decision"] == "D-03"


def test_viewports_default_then_confirmed(tmp_path):
    vp = load_viewports(tmp_path)
    assert vp["confirmed"] is False and set(vp["platforms"]) == {"mobile", "tablet", "web"}
    saved = save_viewports(tmp_path, {"mobile": {"width": 360, "height": 800, "orientation": "portrait"}}, "D-02")
    assert saved["confirmed"] and saved["decision"] == "D-02"
    js = (tmp_path / ".superpowers/ux/kit/viewports.js").read_text()
    assert js.startswith("/*") and '"width": 360' in js and "window.UX_VIEWPORTS" in js
    assert load_viewports(tmp_path)["platforms"]["mobile"]["width"] == 360


def test_cli_viewports_tablet_landscape(tmp_path):
    import argparse
    from coder_nexus.ux.commands import cmd_ux
    args = argparse.Namespace(ux_command="viewports", project=str(tmp_path), platforms="mobile,tablet", mobile="390x844",
                              tablet="820x1180", web=None, tablet_orientation="landscape", decision="D-04", json=False)
    assert cmd_ux(args) == 0
    data = load_viewports(tmp_path)
    assert set(data["platforms"]) == {"mobile", "tablet"}
    assert data["platforms"]["tablet"] == {"width": 1180, "height": 820, "orientation": "landscape"}


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_kit_js_is_valid_javascript():
    js = Path(__file__).resolve().parents[1] / "src/coder_nexus/ux/assets/kit.js"
    res = subprocess.run(["node", "--check", str(js)], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
