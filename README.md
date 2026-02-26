📊 Streamlit Data Visualization (데이터 분석 웹)
사용자가 데이터를 업로드하거나 제공된 데이터셋을 통해 시각적 통찰을 얻을 수 있는 Streamlit 기반 데이터 분석 도구입니다.

🏗️ 시스템 아키텍처

graph TD
    Data[@welfare_2015.csv] --> Logic[@app.py]
    Logic -->|데이터 처리/시각화| Streamlit[Streamlit UI]
    Streamlit -->|상호작용| User((사용자))

    
📂 핵심 코드 가이드
메인 어플리케이션: @app.py에서 전체적인 데이터 처리 로직과 Streamlit UI 구성 요소들이 정의되어 있습니다.
분석 데이터셋: @welfare_2015.csv 파이선 코드에서 로드하여 분석하는 복지 관련 실제 데이터 파일입니다.
환경 설정: @requirements.txt에 적힌 라이브러리들을 설치하여 분석 환경을 즉시 구축할 수 있습니다.
