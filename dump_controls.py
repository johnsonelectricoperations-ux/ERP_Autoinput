from pywinauto import Application
import sys

# ERP 창 연결
app = Application(backend="uia").connect(title="존슨일렉트릭오퍼레이션스")
win = app.top_window()
print("연결 성공:", win.window_text())

# 컨트롤 트리 파일로 저장
output_path = "controls.txt"

with open(output_path, "w", encoding="utf-8") as f:
    original_stdout = sys.stdout
    sys.stdout = f
    win.print_control_identifiers(depth=8)
    sys.stdout = original_stdout

print(f"✅ 완료! {output_path} 저장됨")