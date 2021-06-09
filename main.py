import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image

st.set_page_config(page_title="Streamlit Project Planning", page_icon=':smiley:', layout="centered")

def get_prv_month(yearmonth: str) -> str:
    year_cur = int(yearmonth[:4])
    month_cur = int(yearmonth[4:])
    month_prv = 12 if month_cur==3 else month_cur-3
    year_prv = year_cur-1 if month_cur==3 else year_cur
    return f'{year_prv:04}{month_prv:02}'

def main():
    
    # 메뉴
    menu = st.sidebar.selectbox('메뉴', ['계획', "현황"], index=1)

    # 계획
    if menu == "계획":
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
            ['DB', '202009', '일반', 4000],
            ['DB', '202009', '장기', 14000],
            ['DB', '202009', '자동차', 9000],
            ['DB', '202012', '일반', 5000],
            ['DB', '202012', '장기', 15000],
            ['DB', '202012', '자동차', 10000],
        ], columns=['company', 'base_month', 'lob', 'premium'])

        profit = pd.DataFrame([
            ['DB', '202009', '일반', 400],
            ['DB', '202009', '장기', 1400],
            ['DB', '202009', '자동차', 900],
            ['DB', '202012', '일반', 500],
            ['DB', '202012', '장기', 1500],
            ['DB', '202012', '자동차', 1000],
        ], columns=['company', 'base_month', 'lob', 'profit'])

        asset = pd.DataFrame([
            ['DB', '202009', '현예금및예치금', 40],
            ['DB', '202009', '유가증권', 140],
            ['DB', '202009', '대출채권', 90],
            ['DB', '202009', '부동산', 50],
            ['DB', '202009', '기타자산', 15],
            ['DB', '202012', '현예금및예치금', 50],
            ['DB', '202012', '유가증권', 150],
            ['DB', '202012', '대출채권', 100],
            ['DB', '202012', '부동산', 60],
            ['DB', '202012', '기타자산', 20],
        ], columns=['company', 'base_month', 'account', 'amount'])

        liability = pd.DataFrame([
            ['DB', '202009', '책임준비금', 40],
            ['DB', '202009', '기타부채', 140],
            ['DB', '202012', '책임준비금', 50],
            ['DB', '202012', '기타부채', 150],
        ], columns=['company', 'base_month', 'account', 'amount'])

        capital = pd.DataFrame([
            ['DB', '202009', '자본금', 40],
            ['DB', '202009', '자본잉여금', 40],
            ['DB', '202009', '이익잉여금', 50],
            ['DB', '202012', '자본금', 50],
            ['DB', '202012', '자본잉여금', 50],
            ['DB', '202012', '이익잉여금', 60],
        ], columns=['company', 'base_month', 'account', 'amount'])

        raas = pd.DataFrame([
            ['DB', '202009', '손해율', 2],
            ['DB', '202009', '사업비율', 2],   
            ['DB', '202009', '운용자산이익률', 3],   
            ['DB', '202009', 'RBC비율', 3],   
            ['DB', '202009', '유동성비율', 3],   
            ['DB', '202009', '자산건전성비율', 3],   
            ['DB', '202012', '손해율', 3],
            ['DB', '202012', '사업비율', 2],   
            ['DB', '202012', '운용자산이익률', 3],   
            ['DB', '202012', 'RBC비율', 3],   
            ['DB', '202012', '유동성비율', 4],   
            ['DB', '202012', '자산건전성비율', 5],   
        ], columns=['company', 'base_month', 'account', 'value'])

        # 입력
        col1, col2 = st.beta_columns(2)
        with col1:
            company = st.selectbox('회사', ['DB'])
        with col2:
            base_month = st.selectbox('기준년월', ['202012'])
            prv_month = get_prv_month(base_month)


        # 그림1
        st.header("**Ⅰ. 재무상태**")
        st.markdown("Suspendisse at egestas risus, sed porta massa. Pellentesque consequat tortor purus, quis luctus urna dignissim a. Nulla suscipit odio nec augue tristique, at iaculis orci molestie. Donec viverra sagittis justo et hendrerit. Integer elementum libero diam, et laoreet libero tincidunt non. Etiam nulla mauris, malesuada at ultrices vel, laoreet in nisl. Ut nec maximus orci. Sed quis elit porttitor arcu rutrum dignissim nec vitae odio. Duis dictum ultrices metus placerat porttitor. Duis eget enim vitae mauris faucibus feugiat. Suspendisse vitae porta risus, sit amet hendrerit est. Quisque maximus congue mauris, vel pellentesque quam rhoncus quis. Fusce bibendum justo eu dignissim ornare.")
        fig1 = make_subplots(rows=1, cols=3, specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]])

        ## 자산
        asset_cur = asset.query('base_month==@base_month & company == @company')
        fig1.add_trace(go.Pie(values=asset_cur['amount'], labels=asset_cur['account']), row=1, col=1)

        ## 부채
        liab_cur = liability.query('base_month==@base_month & company == @company')
        fig1.add_trace(go.Pie(values=liab_cur['amount'], labels=liab_cur['account']), row=1, col=2)

        ## 자본
        cap_cur = capital.query('base_month==@base_month & company == @company')
        fig1.add_trace(go.Pie(values=cap_cur['amount'], labels=cap_cur['account']), row=1, col=3)

        st.plotly_chart(fig1)
    

        # 그림2
        st.header("**Ⅱ. 매출 및 손익**")
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget congue dolor, vel suscipit tellus. Morbi scelerisque rutrum urna, elementum tempor erat sodales eu. Vestibulum massa turpis, interdum eget tincidunt non, tincidunt et dolor. Suspendisse ut dui eleifend, ultrices ex ultrices, interdum tellus. Nulla viverra nulla velit, ut dignissim sem sodales efficitur. Quisque fringilla malesuada eros, non blandit quam molestie quis. Aliquam non sem id purus facilisis consectetur ac vestibulum risus. Donec volutpat euismod lectus at ultrices. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum aliquam laoreet urna, sed bibendum augue venenatis eu. Ut ut egestas mi. Nunc quis aliquam libero.")
        fig2 = make_subplots(rows=1, cols=2)

        ## 매출
        prem_cur = premium.query('base_month==@base_month & company == @company')
        prem_prv = premium.query('base_month==@prv_month & company == @company')
        fig2.add_trace(go.Bar(x=prem_prv['lob'], y=prem_prv['premium']), row=1, col=1)
        fig2.add_trace(go.Bar(x=prem_cur['lob'], y=prem_cur['premium']), row=1, col=1)

        ## 손익
        profit_cur = profit.query('base_month==@base_month & company == @company')
        profit_prv = profit.query('base_month==@prv_month & company == @company')
        fig2.add_trace(go.Bar(x=profit_prv['lob'], y=profit_prv['profit']), row=1, col=2)
        fig2.add_trace(go.Bar(x=profit_cur['lob'], y=profit_cur['profit']), row=1, col=2)

        st.plotly_chart(fig2)


        # 그림3
        st.header("**Ⅲ. 경영지표**")
        st.markdown("Etiam sollicitudin magna at metus malesuada sagittis. Nulla lectus purus, suscipit nec leo a, consectetur suscipit lectus. Suspendisse ut orci lobortis, iaculis mauris vitae, feugiat arcu. Phasellus auctor suscipit turpis id pharetra. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse potenti. Etiam rutrum congue sollicitudin. Nullam dictum consequat est ac tristique. Nulla facilisi. Mauris semper orci eu feugiat interdum. Sed facilisis bibendum justo, sed lobortis ligula placerat vitae. Pellentesque sed ex eget erat iaculis lacinia. Quisque nibh nibh, interdum non ex vitae, hendrerit efficitur ipsum. Cras pharetra vitae lorem non euismod. Vestibulum eu scelerisque eros. Nunc non tortor sit amet lorem auctor laoreet.")
        fig3 = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatterpolar'}]])

        ## RAAS등급
        raas_cur = raas.query('base_month==@base_month & company == @company')
        raas_prv = raas.query('base_month==@prv_month & company == @company')
        fig3.add_trace(go.Scatterpolar(r=raas_prv['value'], theta=raas_prv['account'], fill='toself'), row=1, col=1)
        fig3.add_trace(go.Scatterpolar(r=raas_cur['value'], theta=raas_cur['account'], fill='toself'), row=1, col=1)

        st.plotly_chart(fig3)

if __name__ == '__main__':
    main()