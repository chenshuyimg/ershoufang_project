import streamlit as st
import pandas as pd
import plotly.express as px

# 页面配置
st.set_page_config(page_title="重庆二手房数据可视化", layout="wide")

# 读取数据
@st.cache_data
def load_data():
    # ⚠️ 使用你的真实文件名
    df = pd.read_csv("chongqing_100k_simulated.csv")
    return df

df = load_data()

st.title("🏠 重庆二手房市场数据可视化")
st.caption("数据来源：贝壳网（模拟采集） | 数据量：{} 条".format(len(df)))

# ---------------------
# 区域筛选
# ---------------------
districts = sorted(df["district"].dropna().unique())
selected_districts = st.multiselect(
    "选择行政区（可多选）",
    districts,
    default=districts[:5]
)

filtered_df = df[df["district"].isin(selected_districts)]

st.markdown(f"### 当前筛选结果：{len(filtered_df)} 套房源")

# ---------------------
# 房屋基础信息展示
# ---------------------
st.dataframe(filtered_df.head(20), use_container_width=True)

# ---------------------
# 1️⃣ 总价分布
# ---------------------
st.subheader("💰 总价分布（万元）")
fig1 = px.histogram(
    filtered_df,
    x="price_total_wan",
    nbins=50,
    color="district",
    title="各区总价分布"
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------
# 2️⃣ 单价分布
# ---------------------
st.subheader("🏢 单价分布（元/㎡）")
fig2 = px.box(
    filtered_df,
    x="district",
    y="unit_price_cny_per_sqm",
    color="district",
    points="all",
    title="不同区单价箱型图"
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------
# 3️⃣ 面积与价格关系
# ---------------------
st.subheader("📏 面积与总价关系")
fig3 = px.scatter(
    filtered_df,
    x="area_sqm",
    y="price_total_wan",
    color="district",
    size="unit_price_cny_per_sqm",
    hover_data=["title", "rooms", "built_year"],
    title="房屋面积 vs 总价（按单价大小标记）"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------
# 4️⃣ 建成年份分布
# ---------------------
st.subheader("🏗️ 建成年份分布")
fig4 = px.histogram(
    filtered_df,
    x="built_year",
    color="district",
    nbins=40,
    title="不同区房源建成年份分布"
)
st.plotly_chart(fig4, use_container_width=True)

# ---------------------
# 5️⃣ 房型统计
# ---------------------
st.subheader("🛏️ 房型分布（rooms）")
room_counts = (
    filtered_df.groupby(["district", "rooms"])
    .size()
    .reset_index(name="count")
)
fig5 = px.bar(
    room_counts,
    x="rooms",
    y="count",
    color="district",
    barmode="group",
    title="不同区房型数量分布"
)
st.plotly_chart(fig5, use_container_width=True)

# ---------------------
# 页面尾部
# ---------------------
st.markdown("---")
st.caption("© 2025 重庆二手房市场分析可视化 | 由 Streamlit + Plotly 提供支持")
