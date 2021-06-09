import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image

st.set_page_config(page_title="Streamlit Project Planning", page_icon=':smiley:', layout="wide")

def main():
    
    # 메뉴
    menu = st.sidebar.selectbox('메뉴', ['Planning', "현황"], index=1)

    # 계획
    if menu == "Planning":
        st.title("Streamlit Project Planning")

        st.header("**Ⅰ. 개요**")
        st.markdown("""
            * **(목적)** 본 계획서는 Streamlit을 이용한 Dashboard를 만들기 위해 작성
                - 금감원 **금융통계정보시스템**에서 제공하는 Open API를 기초데이터로 사용
            * **(내용)** Dashboard에서 보여주고자 하는 것은 다음의 3가지임
                - 회사의 현재 상태(Statement) 및 실적(Performance))
                - 회사가 과거와 비교했을 때 얼마나 달라졌는지
                - 동업사와 비교했을 때 어떠한지
        """)

        st.header("**Ⅱ. 프로그램 설계**")
        st.subheader("**1. 구성**")
        st.markdown("""
            * **(모듈)** 다음과 같이 3개의 모듈로 구성
            > \- Dashboard에 적용할 조건(기준년월 등) 선택(**main.py**)  
            > \- 시스템에서 데이터 입수(**crawling.py**)  
            > \- 주어진 입력 데이터에 대해 Dashboard 생성(**display.py**)  

            * **(DB)** 일단 DB는 사용하지 않는 것으로 결정
            * **(프로세스)** 다음과 같이 4개의 프로세스를 거침
            > 1) 앱 실행 시 시스템에서 가장 직전 5년치 데이터 수집   
            > 2) 가장 최신일자로 Dashboard 생성  
            > 3) 어떤 조건으로 조회할지 선택할 수 있는 화면 생성  
            > 4) 유저가 조건 선택하고 "생성" 버튼 누르면 조건대로 Dashboard 생성  
        """)

        st.subheader("**2. 생성 주기**")
        st.markdown("""
            * 분기 단위
        """)

        st.subheader("**3. 레이아웃**")
        img = Image.open('img/fig1.png')
        st.image(img)
        st.markdown("""
        * (데이터) 항목별로 아래와 같이 레이아웃 구성
        > 1) 매출(보유보험료): 기준년월(당월/전월), 일장자구분, 금액  
        > 2) 손익: 기준년월(당월/전월), 일장자구분, 손익구분, 금액  
        > 3) 자산: 기준년월(당월/전월), 자산구분, 금액  
        > 4) 부채: 기준년월(당월/전월), 부채구분, 금액  
        > 5) 자본: 기준년월(당월/전월), 자본구분, 금액  
        > 6) 경영지표: 기준년월(당월/전월), 지표구분, 값
        """)


        st.header("** Ⅲ. 개발 순서**")
        st.markdown("""
            1. 임의의 입력값이 주어질 때 Dashboard 만드는 프로그램
            2. 조건 레이아웃 있는 프로그램
            3. 데이터 수집 프로그램
        """)
    
    if menu == "현황":
        # 테스트 데이터
        premium = pd.DataFrame([
            ['202009', '일반', 4000],
            ['202009', '장기', 14000],
            ['202009', '자동차', 9000],
            ['202012', '일반', 5000],
            ['202012', '장기', 15000],
            ['202012', '자동차', 10000],
        ], columns=['base_month', 'lob', 'premium'])

        profit = pd.DataFrame([
            ['202009', '일반', 400],
            ['202009', '장기', 1400],
            ['202009', '자동차', 900],
            ['202012', '일반', 500],
            ['202012', '장기', 1500],
            ['202012', '자동차', 1000],
        ], columns=['base_month', 'lob', 'profit'])

        asset = pd.DataFrame([
            ['202009', '현예금및예치금', 40],
            ['202009', '유가증권', 140],
            ['202009', '대출채권', 90],
            ['202009', '부동산', 50],
            ['202009', '기타자산', 15],
            ['202012', '현예금및예치금', 50],
            ['202012', '유가증권', 150],
            ['202012', '대출채권', 100],
            ['202012', '부동산', 60],
            ['202012', '기타자산', 20],
        ], columns=['base_month', 'account', 'amount'])

        liability = pd.DataFrame([
            ['202009', '책임준비금', 40],
            ['202009', '기타부채', 140],
            ['202012', '책임준비금', 50],
            ['202012', '기타부채', 150],
        ], columns=['base_month', 'account', 'amount'])

        capital = pd.DataFrame([
            ['202009', '자본금', 40],
            ['202009', '자본잉여금', 40],
            ['202009', '이익잉여금', 50],
            ['202012', '자본금', 50],
            ['202012', '자본잉여금', 50],
            ['202012', '이익잉여금', 60],
        ], columns=['base_month', 'account', 'amount'])

        indicators = pd.DataFrame([
            ['202012', '손해율', 90],
            ['202012', '사업비율', 45],   
            ['202012', '운용자산이익률', 2],   
            ['202012', 'RBC비율', 190],   
            ['202012', '유동성비율', 90],   
            ['202012', '자산건전성비율', 20],   
            ['202012', '손해율', 100],
            ['202012', '사업비율', 50],   
            ['202012', '운용자산이익률', 3],   
            ['202012', 'RBC비율', 200],   
            ['202012', '유동성비율', 100],   
            ['202012', '자산건전성비율', 30],   
        ], columns=['base_month', 'account', 'value'])

        col1, col2 = st.beta_columns((2, 1))

        with col1:
            # 그림1
            fig1 = make_subplots(rows=1, cols=2)

            ## 매출
            prem_cur = premium.query('base_month=="202012"')
            prem_prv = premium.query('base_month=="202009"')
            fig1.add_trace(go.Bar(x=prem_prv['lob'], y=prem_prv['premium']), row=1, col=1)
            fig1.add_trace(go.Bar(x=prem_cur['lob'], y=prem_cur['premium']), row=1, col=1)

            ## 손익
            profit_cur = profit.query('base_month=="202012"')
            profit_prv = profit.query('base_month=="202009"')
            fig1.add_trace(go.Bar(x=profit_prv['lob'], y=profit_prv['profit']), row=1, col=2)
            fig1.add_trace(go.Bar(x=profit_cur['lob'], y=profit_cur['profit']), row=1, col=2)

            st.plotly_chart(fig1)

            # 그림2
            fig2 = make_subplots(rows=1, cols=3, specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]])

            ## 자산
            asset_cur = asset.query('base_month=="202012"')
            fig2.add_trace(go.Pie(values=asset_cur['amount'], labels=asset_cur['account']), row=1, col=1)

            ## 부채
            liab_cur = liability.query('base_month=="202012"')
            fig2.add_trace(go.Pie(values=liab_cur['amount'], labels=liab_cur['account']), row=1, col=2)

            ## 자본
            cap_cur = capital.query('base_month=="202012"')
            fig2.add_trace(go.Pie(values=cap_cur['amount'], labels=cap_cur['account']), row=1, col=3)

            st.plotly_chart(fig2)
        
        with col2:
            # 그림3
            fig3 = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatterpolar'}]])

            ## 경영효율지표
            indi_cur = indicators.query('base_month=="202012"')
            indi_prv = indicators.query('base_month=="202009"')
            fig3.add_trace(go.Scatterpolar(r=indi_prv['value'], theta=indi_prv['account'], fill='toself'), row=1, col=1)
            fig3.add_trace(go.Scatterpolar(r=indi_cur['value'], theta=indi_cur['account'], fill='toself'), row=1, col=1)

            st.plotly_chart(fig3)

if __name__ == '__main__':
    main()