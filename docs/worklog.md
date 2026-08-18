# 작업 기록 (worklog)

## 2026-08-18
- 목표
  1. venv에만 설치되어 있던 라이브러리를 `requirements.txt`로 정리 (다른 PC 재현용)
  2. 현행 근태 자동입력 스크립트를 **부서별 다중 메뉴 + 야간 무인 실행** 시스템으로 확장하는 구상안 작성
- 완료
  - `requirements.txt` 생성 — 코드에서 실제 import 되는 `pywinauto`, `openpyxl` 확인 후 정리
  - `.gitignore` 생성 — venv/`__pycache__` 커밋 방지
  - `docs/자동입력_시스템_2.0_구상안.md` 작성 (설계안, 구현 아님)
- 조사로 알아낸 것 (다음 세션에서 재조사 불필요)
  - `controls.txt` 상 ERP는 **WPF 앱**이며 컨트롤이 UIA 트리에 정상 노출됨
    → 좌표 클릭 없이 `ValuePattern.SetValue` / `SelectionItemPattern.Select` / `InvokePattern.Invoke`로 입력 가능
  - 메인 윈도우 클래스명이 `AngKor.Ylw.Main.Formlib` → **영림원소프트랩 K-System 계열로 추정**
    (Ylw = YoungLimWon). 벤더 엑셀업로드/OpenAPI 존재 여부 확인이 최우선 과제
  - `auto_id` 명명 규칙이 일관됨: `txt*`(Edit) / `cmb*`(ComboBox) / `dat*`(날짜) / `msk*`(시간) / `flt*`(숫자)
    → 필드 타입 자동 추론 가능
  - 메뉴 이동 수단 3가지 확인: `PART_txtPgmSearch`(프로그램 검색창, 가장 견고) / `cmbModule` + `treeview` / `Favorites`
- 다음 할 일
  - 사용자에게 확인 요청한 7개 질문 답변 대기 (구상안 10장). 특히 **질문 1(벤더 인터페이스 유무)** 이 설계 방향을 결정함
  - 답변 후 Phase 1 착수: 어댑터 골격 + 레시피 로더 + 기존 근태 화면을 YAML로 재현해 현행과 결과 동일함 검증
- 주의
  - 구상안은 **설계 문서일 뿐 구현이 아님.** 코드는 아직 현행 4개 스크립트 그대로임
  - ERP 실물이 없는 원격 환경이라 UIA 동작은 실제 검증 불가. Phase 1은 반드시 실 PC에서 dry-run으로 확인할 것
  - 실 데이터 입력 자동화이므로 부서 확산 시 최소 1주 수기 병행 대조 후 단독 전환 권장
