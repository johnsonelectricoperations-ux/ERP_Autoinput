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
- 사용자 확인 완료 사항 (구상안 v2에 반영됨)
  1. 벤더 대량입력 수단(API/엑셀업로드) → **사용 불가** ⇒ UIA 화면 자동화로 확정
  2. ERP 로그인 → ERP 첫 화면에서 **ID/PW 직접 입력**, PC 비밀번호와 별개. SSO/OTP 아님
     ⇒ 자동 로그인 구현 가능. 단 로그인 화면 컨트롤 auto_id는 아직 미확보
  3. 운영 PC → **화면보호기가 자동 실행됨.** OS/GPO 설정은 그대로 두고(협의 불필요),
     프로그램 실행 중에만 마우스를 주기적으로 움직여 방지하는 방식
     ⇒ 커서를 실제로 움직이면 자동화 클릭과 충돌하므로 `mouse_event(MOUSEEVENTF_MOVE, 0, 0)`
        (커서 위치 불변 + 유휴 타이머만 리셋)로 구현하기로 설계
     ⇒ **각성 유지는 실행 시작~종료 전 구간 상시 동작.** "자동화 가동 중에는 불필요"가 아님 —
        UIA 패턴(ValuePattern.SetValue)은 입력 큐를 거치지 않는 COM 호출이라
        Windows 유휴 타이머(GetLastInputInfo)를 리셋하지 않음. 즉 100건을 입력하며 30분을 돌아도
        Windows는 "유휴"로 판단함. 게다가 ERP 기동 대기·파일 이동·리포트 생성 구간은 무입력임
  4. 소스파일 → 부서별 공용폴더에 각 양식, **양식은 새로 개발해도 됨**
     ⇒ 레시피 YAML에서 엑셀 양식을 자동 생성하는 구조로 설계 (양식·검증·입력이 한 정의에서 파생)
- 다음 할 일
  - 남은 질문 6개 답변 대기 (구상안 11장). 특히 **`ScreenSaverIsSecure` 레지스트리 값**이
    야간 무인 실행 성립 여부를 가르는 핵심 (1이면 화면보호기 = 세션 잠금 = 자동화 실패)
  - Phase 1 착수: 레시피 로더 + `fields.py` 3단 폴백 + 기존 근태 화면을 YAML로 재현해
    현행과 결과 동일함 검증
- 주의 (추가)
  - **컨트롤별로 UIA ValuePattern이 먹히는지 실측 필요.** WPF 마스크/날짜 컨트롤 일부는
    ValuePattern을 노출하지 않을 수 있음 → Phase 1에서 측정해 레시피에 write_mode로 고정
  - **Phase 2 완료 판정은 "화면보호기 대기시간을 2분으로 줄이고 30분 방치 테스트 통과"로 고정.**
    이 검증을 건너뛰면 실제 야간 운영 첫날 실패함
- 주의
  - 구상안은 **설계 문서일 뿐 구현이 아님.** 코드는 아직 현행 4개 스크립트 그대로임
  - ERP 실물이 없는 원격 환경이라 UIA 동작은 실제 검증 불가. Phase 1은 반드시 실 PC에서 dry-run으로 확인할 것
  - 실 데이터 입력 자동화이므로 부서 확산 시 최소 1주 수기 병행 대조 후 단독 전환 권장
