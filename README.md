# pygame-tutorial

## 파이썬 가상환경의 준비 (Windows)

1. 폴더를 하나 만드세요
2. 원도우 터미널을 시작하고 위에서 만든 폴더로 이동하세요
   - `cmd`
   - `cd <folder_name>`
3. 파이썬 가상환경을 만드세요
   - `py -m venv .env`
4. 파이썬 가상환경을 시작하세요
   - `%CD%\.env\activate.bat`
5. `pip`을 최신 버전으로 업그레이드하세요
   - `python -m pip install -U pip`
6. `pip`을 통해 `pygame`을 설치하세요
   - `pip install pygame`

> 코드 에디터에서 `formatter`를 사용한다면, `autopep8`을 설치하세요
>
> - `pip install autopep8`

## 강의 순서

1. 파이썬 가상환경 준비 및 pygame 설치
2. pygame 앱 시작하기
3. `안녕하세요` 출력하기
   - 폰트 사용하기
4. 15 퍼즐 보드 그리기
5. 게임 초기화하기
   - 해결 가능한 게임이어야 함
6. 키보드 입력 읽기
   - 방향키 입력받기
7. 마우스 입력 읽기
   - 좌클릭한 퍼즐 조각 인덱스 출력
8. 퍼즐 조각 움직이기
   - 좌클릭한 퍼즐 조각 순간이동하기
   - 이동 불가능한 경우, 아무것도 안하기
9. 퍼즐 조각 움직이기
   - 키보드 방향기로 퍼즐 조각 빈 공간으로 순간이동하기
10. 퍼즐 조각 이동 에니메이션
    - 이동 가능한 경우
11. 퍼즐 조각 이동 에니메이션
    - 이동 불가능한 경우
12. 퍼즐이 완성되었는지 확인하기
13. 배경 이미지 사용하기
14. 퍼즐 조각 위에 숫자 대신 이미지 이용하기
15. 오디오 사용하기
16. 메뉴와 게임 정보 보여주기 (예: 이동수)
17. 게임 꾸미기
