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
- 추가 요청: **웹 대시보드**(실행 내역·진행 상황·자동화 항목 설정) → 구상안 10장으로 추가
  - Runner(야간 배치)와 Web(상시 서비스)을 **별도 프로세스로 분리**, state.db(WAL)로만 통신
    ⇒ 웹이 죽어도 야간 자동화는 정상 동작해야 함
  - 기술 스택: FastAPI + Jinja2 + htmx (React는 npm 빌드 파이프라인 때문에 제외), NSSM으로 서비스 등록
  - 설정 편집은 안전 등급 분리: 🟢 활성여부·시각·한도 = 자유 / 🔴 auto_id 매핑·save_verify = 조회만
  - 순서: 읽기전용 대시보드는 Phase 3.5(3~4일), 전체 웹앱은 Phase 6(2~3주)
  - **Runner에 선반영 필요 4가지**: ① 진행상황을 콘솔이 아닌 state.db에 기록 ② 하트비트 10초 주기
    ③ 킬스위치를 DB 플래그로도 확인 ④ 검증 로직을 validator.py로 분리(웹 업로드 화면에서 재사용)
- ★ 운영 PC 잠금 정책 실측 결과 (2026-08-19) — **구상안 6.5에 전문 기록**
  - `HKCU\Control Panel\Desktop` → `ScreenSaveActive=1`, 나머지 값 비어 있음
  - **`HKCU\Software\Policies\Microsoft\Windows\Control Panel\Desktop` (GPO)**
    → `ScreenSaveActive=1` / `ScreenSaveTimeOut=600` / **`ScreenSaverIsSecure=1`**
    / `SCRNSAVE.EXE=C:\Program Files\JE\scrnsave.scr` (회사 자체 제작 화면보호기)
  - **`HKLM\...\Policies\System\InactivityTimeoutSecs=900`** (유휴 15분 강제 잠금, 독립된 2차 잠금)
  - 결론: **유휴 10분 → 화면보호기 → 세션 잠금**이 GPO로 강제됨.
    레지스트리를 직접 고쳐도 GPO 갱신 주기(90분±30분)마다 되돌아오므로 **6.4 방식은 적용 불가**
  - 단, 두 정책 모두 **유휴 시간 기준**이라 유휴 타이머를 60초마다 리셋하면 방어됨 (마진 10배)
  - ⚠️ 이로써 **지글러가 시스템의 급소**가 됨. 지글러가 멈추면 10분 뒤 세션 잠금 = 하루 작업 사망
    ⇒ 지글러 생존 감시(120초 이상 미갱신 시 중단+알림) · 매 건 잠금 감지 · 크래시 시 알림 추가
  - ⚠️ 유휴 타이머 리셋은 회사의 "자리비움 시 잠금" 정책을 무력화하는 동작이므로
    **IT/보안 담당 사전 합의 필요.** 정책 예외 OU로 빼는 것이 더 깔끔한 정공법
  - 협의 불가 시 대안: **업무시간 중 실행** (사람이 PC를 쓰면 유휴가 안 쌓여 정책과 무충돌.
    ERP도 이미 로그인돼 있어 로그인 자동화까지 불필요해짐. 단 ERP 창 점유 충돌은 해결 필요)
- 다음 할 일
  - 남은 질문 (구상안 12장) 답변 대기. 2번은 위와 같이 부분 해소, GPO 정책 경로 확인만 남음
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
