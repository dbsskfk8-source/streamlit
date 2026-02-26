import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# 1. 웹 페이지 설정
st.set_page_config(layout="wide", page_title="복지패널 데이터 분석 대시보드")

# 한글 폰트 설정 (배포 환경에 따라 나눔고딕 등을 권장하지만, 일단 노트북 설정을 유지합니다)
plt.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

# 2. 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data(file_path):
    # 데이터 불러오기
    raw_welfare = pd.read_csv(file_path)
    welfare = raw_welfare.copy()
    
    # 변수명 변경
    welfare = welfare.rename(columns={
        'h10_g3': 'sex',
        'h10_g4': 'birth_year',
        'h10_g10': 'marital_status',
        'h10_g11': 'religion',
        'h10_eco9': 'job_code',
        'p1002_8aq1': 'income',
        'h10_reg7': 'region_code'
    })

    # 전처리 - 성별
    welfare['sex'] = np.where(welfare['sex'] == 9, np.nan, welfare['sex'])
    welfare['sex'] = welfare['sex'].map({1: 'male', 2: 'female'})

    # 전처리 - 월급
    welfare['income'] = welfare['income'].replace(9999, np.nan)
    welfare['income'] = np.where(welfare['income'] == 0, np.nan, welfare['income'])

    # 전처리 - 나이 및 연령대
    welfare['birth_year'] = welfare['birth_year'].replace(9999, np.nan)
    welfare['age'] = 2015 - welfare['birth_year'] + 1
    
    def get_age_group(age):
        if pd.isna(age): return np.nan
        if age >= 60: return "old"
        if age >= 30: return "middle"
        return "young"
    
    welfare['age_group'] = welfare['age'].apply(get_age_group)
    
    return welfare

# 3. 메인 화면 구성
st.title("📊 한국복지패널 데이터 대시보드")

# 파일 업로드 또는 경로 지정 (사용자가 올린 파일명 기준)
DATA_FILE = "welfare_2015_copy.csv"

try:
    df = load_data(DATA_FILE)
    st.success(f"데이터 로드 완료: {df.shape[0]}행 {df.shape[1]}열")
except Exception as e:
    st.error(f"데이터 파일을 찾을 수 없습니다. 파일명이 '{DATA_FILE}'인지 확인해주세요.")
    st.stop()

# 4. 사이드바 필터
st.sidebar.header("🔍 데이터 필터")
selected_sex = st.sidebar.multiselect("성별 선택", options=['male', 'female'], default=['male', 'female'])
age_range = st.sidebar.slider("연령 범위", int(df['age'].min()), int(df['age'].max()), (20, 70))

# 필터링 적용
filtered_df = df[
    (df['sex'].isin(selected_sex)) & 
    (df['age'] >= age_range[0]) & 
    (df['age'] <= age_range[1])
]

# 5. 시각화 섹션
tab1, tab2 = st.tabs(["성별 월급 차이", "나이와 월급 관계"])

with tab1:
    st.subheader("1. 성별에 따른 평균 월급")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sex_income = filtered_df.dropna(subset=['sex', 'income']).groupby('sex', as_index=False).agg(mean_income=('income', 'mean'))
        fig, ax = plt.subplots()
        sns.barplot(x='sex', y='mean_income', data=sex_income, ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.write("집계 테이블")
        st.dataframe(sex_income)

with tab2:
    st.subheader("2. 나이에 따른 월급 변화")
    age_income = filtered_df.dropna(subset=['age', 'income']).groupby('age', as_index=False).agg(mean_income=('income', 'mean'))
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='age', y='mean_income', data=age_income, ax=ax2)
    st.pyplot(fig2)