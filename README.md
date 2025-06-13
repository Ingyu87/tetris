# 🎮 학생들과 함께하는 테트리스 게임

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

교육용으로 제작된 웹 기반 테트리스 게임입니다. 학생들이 함께 플레이하고 경쟁할 수 있는 기능을 제공합니다.

## ✨ 주요 기능

### 🎯 게임 기능
- **3가지 난이도**: Easy, Normal, Hard 모드
- **30단계 레벨 시스템**: 점진적 난이도 증가
- **실시간 점수 계산**: 라인 클리어 보너스
- **다양한 테트리스 블록**: 7가지 클래식 블록

### 🏆 경쟁 시스템
- **실시간 순위표**: 전체 및 모드별 랭킹
- **점수 기록 저장**: 영구적인 기록 관리
- **학생별 성과 추적**: 개인 진행 상황 확인

### 🎮 조작법
- **←/→**: 좌우 이동
- **↑**: 블록 회전
- **↓**: 빠른 낙하
- **스페이스**: 즉시 낙하

## 🚀 빠른 시작

### 필수 요구사항
- Python 3.8 이상
- pip 패키지 매니저

### 설치 및 실행

1. **저장소 복제**
   ```bash
   git clone https://github.com/Ingyu87/tetris-game.git
   cd tetris-game
   ```

2. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **환경 설정 (선택사항)**
   ```bash
   cp .env.example .env
   # .env 파일을 편집하여 설정 변경
   ```

4. **게임 실행**
   ```bash
   streamlit run app.py
   ```

5. **브라우저에서 게임 접속**
   - 자동으로 브라우저가 열리거나
   - http://localhost:8501 접속

## 📁 프로젝트 구조

```
tetris-game/
├── app.py              # 메인 Streamlit 앱
├── requirements.txt    # Python 패키지 목록
├── .env.example       # 환경 변수 템플릿
├── .gitignore         # Git 무시 파일
├── README.md          # 프로젝트 문서
└── scores.json        # 점수 데이터 (자동 생성)
```

## 🎓 교육적 활용

### 수업 활용 방안
- **논리적 사고력**: 블록 배치 전략 수립
- **공간 인식능력**: 2D 공간에서의 블록 조작
- **반응속도**: 빠른 의사결정과 실행
- **경쟁 학습**: 건전한 경쟁을 통한 동기부여

### 평가 요소
- 최고 점수 달성
- 도달한 최고 레벨
- 게임 플레이 시간
- 라인 클리어 효율성

## 🔧 커스터마이징

### 게임 설정 변경
`.env` 파일에서 다음 설정들을 조정할 수 있습니다:

```bash
# 게임 제목 변경
GAME_TITLE=우리반 테트리스 대회

# 최대 참가자 수
MAX_PLAYERS=50

# 기본 게임 모드
DEFAULT_MODE=Easy
```

### 점수 시스템 수정
`app.py` 파일에서 점수 계산 로직을 수정할 수 있습니다.

## 🤝 기여하기

1. 저장소를 Fork 합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/새기능`)
3. 변경사항을 커밋합니다 (`git commit -am '새기능 추가'`)
4. 브랜치에 Push 합니다 (`git push origin feature/새기능`)
5. Pull Request를 생성합니다

## 📊 데이터 관리

### 점수 데이터
- 파일 위치: `scores.json`
- 자동 백업: 환경 설정에서 활성화 가능
- 데이터 포맷: JSON (타임스탬프, 이름, 점수, 레벨, 모드)

### 데이터 초기화
```bash
# 모든 점수 기록 삭제
rm scores.json
```

## 🔍 문제 해결

### 자주 발생하는 문제

**Q: 게임이 로드되지 않아요**
- A: 브라우저를 새로고침하거나 다른 브라우저를 시도해보세요

**Q: 점수가 저장되지 않아요**
- A: 프로젝트 폴더에 쓰기 권한이 있는지 확인하세요

**Q: 키보드 조작이 안 돼요**
- A: 게임 화면을 클릭한 후 키보드를 사용하세요

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👨‍💻 제작자

- **개발자**: Ingyu87
- **이메일**: [연락처]
- **GitHub**: [@Ingyu87](https://github.com/Ingyu87)

## 🙏 감사의 말

이 프로젝트는 교육 목적으로 제작되었으며, 학생들의 학습에 도움이 되기를 바랍니다.

---

**⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요!**