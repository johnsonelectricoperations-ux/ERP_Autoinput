from pywinauto import Desktop

# 현재 열려있는 모든 창 목록 출력
desktop = Desktop(backend="uia")

print("=" * 50)
print("현재 열린 창 목록")
print("=" * 50)

for win in desktop.windows():
    title = win.window_text().strip()
    if title:  # 제목 없는 창 제외
        print(repr(title))

print("=" * 50)