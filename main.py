import json
import urllib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image

# 환경설정
# DB: 0010636, 삼성: 0010633, 현대: 0010634, KB: 0010635, 메리츠: 0010626
# (SI003) A11: 현예금, A12: 유가증권, A14: 대출채권, A15: 부동산, A21: 고정자산, A22: 기타자산, A3: 특별계정자산
AUTH = '7774090942ede970746a7cd9b2e10577'
st.set_page_config(page_title="손해보험회사 현황 대시보드", page_icon=':smiley:', layout="centered")

# 사용자정의 함수
def get_comp_code(company: str) -> str:
    comp_mapper = {'DB': '0010636', '삼성': '0010633', '현대': '0010634', 'KB': '0010635', '메리츠': '0010626'}
    return comp_mapper.get(company)

def get_prv_month(yearmonth: str) -> str:
    year_cur = int(yearmonth[:4])
    month_cur = int(yearmonth[4:])
    month_prv = 12 if month_cur==3 else month_cur-3
    year_prv = year_cur-1 if month_cur==3 else year_cur
    return f'{year_prv:04}{month_prv:02}'

def get_stats(service: str, params: dict = {}) -> pd.DataFrame:
    if service == 'companySearch':
        params['partDiv'] = 'I'
    elif service == 'statisticsListSearch':
        params['lrgDiv'] = 'I'
    params['lang'] = 'kr'
    params['auth'] = AUTH
    tmp = []
    for k, v in params.items():
        tmp.append(k + "=" + v)
    query = '&'.join(tmp)
    url = f'http://fisis.fss.or.kr/openapi/{service}.json?{query}'
    res = urllib.request.urlopen(url)
    data = json.loads(res.read())
    df = pd.DataFrame(data['result']['list'])
    return df

def main():
    
    # 메뉴
    menu = st.sidebar.selectbox('메뉴', ['계획', "회사현황"], index=1)

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

        st.header("** Ⅳ. TODO**")
        st.markdown("""
            * (2021.06.09) 시각화 다듬기
            * (2021.06.09) 리포트 문구 만들기
            * (2021.06.09) 헤로쿠 배포
            * (2021.06.09) 항목 추가하기
        """)
    
    if menu == "회사현황":
        st.markdown("<h1 style='text-align: center; color: black;'><b>회사현황</b></h1><br>", unsafe_allow_html=True)

        # 입력
        col1, col2 = st.beta_columns(2)
        with col1:
            company = st.selectbox('회사', ['삼성', 'DB', '현대', 'KB', '메리츠'])
        with col2:
            base_month = st.selectbox('기준년월', ['202012', '202009', '202006', '202003', '201912'], index=0)
            prv_month = get_prv_month(base_month)
        
        # 공통 매개변수
        params = {}
        params['term'] = 'Q'
        params['startBaseMm'] = prv_month
        params['endBaseMm'] = base_month
        params['financeCd'] = get_comp_code(company)

        # 데이터 수집
        # company_list = get_stats('companySearch')
        # rpt_list = get_stats('statisticsListSearch')
        
        # 자산
        params['listNo'] = 'SI003'
        asset = get_stats('statisticsInfoSearch', params) \
            .query('account_cd in ["A11", "A12", "A14", "A15", "A21", "A22", "A3"]') \
            .astype({'a': float}) \
            .assign(account = lambda x: x.account_nm.str.replace('[(|)| |ㆍ]', '', regex=True)) \
            .assign(a = lambda x: np.round(x.a/1e12,1)) \
            .assign(company = company) \
            .rename(columns={'a': 'amount'}) \
            .filter(['company', 'base_month', 'account', 'amount'], axis=1)

        # 매출
        params['listNo'] = 'SI138'
        premium = get_stats('statisticsInfoSearch', params) \
            .query('account_nm != "합계"') \
            .astype({'a': float}) \
            .assign(a = lambda x: np.round(x.a/1e12,1)) \
            .assign(company = company) \
            .rename(columns={'a': 'amount', 'account_nm': 'lob'}) \
            .filter(['company', 'base_month', 'lob', 'amount'], axis=1)

        # 수익
        params['listNo'] = 'SI137'
        profit = get_stats('statisticsInfoSearch', params) \
            .query('account_nm not in ["당기순이익", "보험손익"]') \
            .astype({'a': float}) \
            .assign(account_nm = lambda x: x.account_nm.str.replace('_', '(', regex=True)) \
            .assign(account_nm = lambda x: x.account_nm.str.replace('보험$', ')', regex=True)) \
            .assign(a = lambda x: np.round(x.a/1e8,1)) \
            .assign(company = company) \
            .rename(columns={'a': 'amount', 'account_nm': 'lob'}) \
            .filter(['company', 'base_month', 'lob', 'amount'], axis=1)

        # 경영효율지표        
        params['listNo'] = 'SI114'
        indicator = get_stats('statisticsInfoSearch', params) \
            .query('account_nm in ["경과손해율", "순사업비율", "운용자산이익률", "영업이익률", "총자산순이익률"]') \
            .astype({'a': float}) \
            .assign(company = company) \
            .rename(columns={'a': 'value', 'account_nm': 'account'}) \
            .pivot_table(index='account', columns='base_month', values='value', aggfunc=np.sum) \
            .filter([prv_month, base_month], axis=1) \
            .assign(증감 = lambda x: np.round(x[base_month] - x[prv_month], 2)) \
            .rename(columns={prv_month: f'\'{prv_month[2:4]}.{prv_month[4:]}', base_month: f'\'{base_month[2:4]}.{base_month[4:]}'}) \
            .rename_axis('항목').reset_index()

        # 손익발생원천분석(TODO: 추가 작업)
        # params['listNo'] = 'SI132'
        # df = get_stats('statisticsInfoSearch', params)
        # st.dataframe(df)

        # 부채
        params['listNo'] = 'SI004'
        liability = get_stats('statisticsInfoSearch', params) \
            .query('account_cd in ["A1111", "A1112", "A1113", "A1114", "A1115", "A1116", "A1117", "A1118", "A12"]') \
            .assign(account_nm = lambda x: x.account_nm.str.replace('보험계약준비금_책임준비금_', '', regex=True)) \
            .assign(a = lambda x: np.round(np.where(x.a==' ', '0', x.a).astype(float)/1e12,1)) \
            .assign(company = company) \
            .rename(columns={'a': 'amount', 'account_nm': 'account'}) \
            .filter(['company', 'base_month', 'account', 'amount'], axis=1)

        # 자본
        params['listNo'] = 'SI004'
        capital = get_stats('statisticsInfoSearch', params) \
            .query('account_cd in ["A21", "A22", "A23", "A24", "A25", "A26", "A27"]') \
            .assign(account = lambda x: x.account_nm.str.replace('\s', '', regex=True)) \
            .assign(company = company) \
            .assign(a = lambda x: np.round(np.where(x.a==' ', '0', x.a).astype(float)/1e12,1)) \
            .rename(columns={'a': 'amount'}) \
            .filter(['company', 'base_month', 'account', 'amount'], axis=1)


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
        fig2.add_trace(go.Bar(x=prem_prv['lob'], y=prem_prv['amount']), row=1, col=1)
        fig2.add_trace(go.Bar(x=prem_cur['lob'], y=prem_cur['amount']), row=1, col=1)

        ## 손익
        profit_cur = profit.query('base_month==@base_month & company == @company')
        profit_prv = profit.query('base_month==@prv_month & company == @company')
        fig2.add_trace(go.Bar(x=profit_prv['lob'], y=profit_prv['amount']), row=1, col=2)
        fig2.add_trace(go.Bar(x=profit_cur['lob'], y=profit_cur['amount']), row=1, col=2)

        st.plotly_chart(fig2)


        # 그림3
        st.header("**Ⅲ. 경영효율지표**")
        st.markdown("Etiam sollicitudin magna at metus malesuada sagittis. Nulla lectus purus, suscipit nec leo a, consectetur suscipit lectus. Suspendisse ut orci lobortis, iaculis mauris vitae, feugiat arcu. Phasellus auctor suscipit turpis id pharetra. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse potenti. Etiam rutrum congue sollicitudin. Nullam dictum consequat est ac tristique. Nulla facilisi. Mauris semper orci eu feugiat interdum. Sed facilisis bibendum justo, sed lobortis ligula placerat vitae. Pellentesque sed ex eget erat iaculis lacinia. Quisque nibh nibh, interdum non ex vitae, hendrerit efficitur ipsum. Cras pharetra vitae lorem non euismod. Vestibulum eu scelerisque eros. Nunc non tortor sit amet lorem auctor laoreet.")
        fig3 = make_subplots(rows=1, cols=1, specs=[[{'type': 'table'}]])

        ## 경영효율지표
        fig3.add_trace(go.Table(
            header=dict(values=list(indicator.columns)),
            cells=dict(values=[indicator.iloc[:, 0], indicator.iloc[:, 1], indicator.iloc[:, 2], indicator.iloc[:, 3]])
        ), row=1, col=1)  

        st.plotly_chart(fig3)

if __name__ == '__main__':
    main()