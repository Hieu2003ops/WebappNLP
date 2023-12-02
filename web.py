import streamlit as st
from streamlit_option_menu import option_menu
from numerize import numerize
import json
import numpy as np
from keras.preprocessing.text import tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import urllib
from tqdm import tqdm
from pyvi import ViTokenizer

# background color
def set_bg_and_text_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: bisque;
        }
        h1 {
            color: black;
        }
        /* Change the header background */
        header .st-ck {
            background-color: bisque;
        }
        /* Change the color of header text if needed */
        header .st-ck .st-bj {
            color: black;
        }
        /* Additional selectors for other text elements you want to change */
        </style>
        """,
        unsafe_allow_html=True
    )

# Define preprocessing function
def vns_preprocessing(line):
    line = line.strip()
    for sc in SPEC_CHARS:
        line = line.replace(sc, ' ')
    line = str(ViTokenizer.tokenize(line))
    words = line.split()
    words = [w for w in words if w.lower() not in STOP_WORDS]
    return ' '.join(words)

# predict def
def predict_sentiment(user_input):
    try:
        text = vns_preprocessing(user_input)
        sequences_test = tokenizer.texts_to_sequences([text])
        sequences_padded = pad_sequences(sequences_test, maxlen=128, padding='post', truncating='post')

        # Dự đoán từ cả hai models
        prediction1 = model1.predict(sequences_padded)
        prediction2 = model2.predict(sequences_padded)
        prediction3 = model3.predict(sequences_padded)
        # Chuyển đổi số thành chuỗi tương ứng cho model1 và model2
        output1 = 'Negative' if np.argmax(prediction1, axis=1) == 0 else 'Neutral or Not Mentioned' if np.argmax(prediction1, axis=1) == 1 else 'Positive'
        output2 = 'Negative' if np.argmax(prediction2, axis=1) == 0 else 'Neutral or Not Mentioned' if np.argmax(prediction2, axis=1) == 1 else 'Positive'
        output3 = 'Negative' if np.argmax(prediction3, axis=1) == 0 else 'Neutral or Not Mentioned' if np.argmax(prediction3, axis=1) == 1 else 'Positive'

        # Trả về kết quả từ cả hai models với tiêu đề tương ứng
        return "Describe product: " + output1, "Quality product: " + output2 , "Shipping product: " + output3
    except Exception as e:
        return f"An error occurred: {e}"
    
# Define display_result_with_emoji function  
def display_result_with_emoji(title, output):
    emoji = ''
    if 'Positive' in output:
        emoji = '😊'  # Happy emoji for positive sentiment
    elif 'Negative' in output:
        emoji = '😟'  # Sad emoji for negative sentiment
    else:  # Neutral or Not Mentioned
        emoji = '😐'  # Neutral face emoji for neutral sentiment

    st.success(f"{title} {output} {emoji}")

# Load models
model1 = load_model("sentiment_describes.h5")
model2 = load_model("sentiment_qualities.h5")
model3 = load_model("sentiment_shipping.h5")

# Load tokenizer
with open('tokenizer.json', 'r', encoding='utf-8') as f:
    tokenizer = tokenizer_from_json(json.load(f))

#Khai báo stopword
STOP_WORDS = set("""
a
b
c
d
đ
e
f
g
h
i
j
k
l
m
n
o
p
q
r
s
t
u
v
w
x
z
ii
iii
iv
vii
viii
ix
wi
xj
ng
cij
bij
aji
a_ha
xt
xm
amn
am
ab
ac
bt
at
bh
ah
xiyi
yt
ax
bi_ai
rm
xn
nxn
bn
aij
aa
xxi
a_an
uti
uj
u_i
ux
ut
u_t
u_y
u_u
um
u_x
y_y
oe
ou
xf
rk
t_a
a_t
t_x
p_x
gr
dxdy
dx
dy
p_y
px
pp
yy
tz
t_dt
xk
p_k
p_xn
bằng_không
bằng_người
bằng_như
bằng_nào
bằng_nấy
bằng_vào
bằng_được
bằng_ấy
bởi_ai
bởi_chưng
bởi_nhưng
bởi_sao
bởi_thế
bởi_thế_cho_nên
bởi_tại
bởi_vì
bởi_vậy
bởi_đâu
chắc_chắn
chắc_dạ
chắc_hẳn
chắc_lòng
chắc_người
chắc_vào
chắc_ăn
chẳng_lẽ
chẳng_những
chẳng_nữa
chẳng_phải
chỉ_chính
chỉ_có
chỉ_là
chỉ_tên
chứ_gì
chứ_không
chứ_không_phải
chứ_lại
chứ_lị
chứ_như
chứ_sao
cũng_như
cũng_nên
cũng_thế
cũng_vậy
cũng_vậy_thôi
cũng_được
cơ_chỉ
cơ_chừng
cơ_dẫn
cơ_hồ
cơ_mà
cứ_như
cứ_việc
cứ_điểm
cực_lực
dù_cho
dù_dì
dù_gì
dù_rằng
dù_sao
dẫu_mà
dẫu_rằng
dẫu_sao
dễ_gì
dễ_khiến
dễ_nghe
dễ_như_chơi
hay_biết
hay_hay
hay_không
hay_là
hay_làm
hay_nhỉ
hay_nói
hay_sao
hay_tin
hay_đâu
hoặc_là
hãy_còn
hơn_cả
hơn_hết
hơn_là
hơn_nữa
hơn_trước
hầu_hết
là_cùng
là_là
là_nhiều
là_phải
là_thế_nào
là_vì
là_ít
lâu_các
lâu_lâu
lâu_nay
lâu_ngày
lại_còn
lại_giống
lại_làm
lại_người
lại_nói
lại_nữa
lại_thôi
lại_ăn
lại_đây
mà_cả
mà_không
mà_lại
mà_thôi
mà_vẫn
mất_còn
mọi_giờ
mọi_khi
mọi_lúc
mọi_người
mọi_nơi
mọi_sự
mọi_thứ
mọi_việc
mỗi_lúc
mỗi_lần
mỗi_một
mỗi_ngày
mỗi_người
như_ai
như_chơi
như_không
như_là
như_nhau
như_quả
như_sau
như_thường
như_thế
như_thế_nào
như_thể
như_trên
như_trước
như_tuồng
như_vậy
như_ý
nhưng_mà
nhược_bằng
nhằm_khi
nhằm_lúc
nhằm_vào
nhằm_để
những_ai
những_khi
những_là
những_lúc
những_muốn
những_như
nào_cũng
nào_hay
nào_là
nào_phải
nào_đâu
nào_đó
nên_chi
nên_chăng
nên_làm
nên_người
nên_tránh
nếu_có
nếu_cần
nếu_không
nếu_mà
nếu_như
nếu_thế
nếu_vậy
nếu_được
nữa_khi
nữa_là
nữa_rồi
quả_là
quả_thật
quả_thế
quả_vậy
thà_là
thà_rằng
thì_giờ
thì_là
thì_phải
thì_ra
thì_thôi
thường_hay
thường_khi
thường_số
thường_sự
thường_thôi
thường_thường
thường_tính
thường_tại
thường_xuất_hiện
thường_đến
thật_chắc
thật_là
thật_lực
thật_quả
thật_ra
thật_sự
thật_thà
thật_tốt
thật_vậy
thế_là
thế_lại
thế_mà
thế_nào
thế_nên
thế_ra
thế_sự
thế_thì
thế_thôi
thế_thường
thế_thế
thế_đó
vậy_là
vậy_mà
vậy_nên
vậy_ra
vậy_thì
vậy_ư
với_lại
với_nhau
vừa_khi
vừa_lúc
vừa_mới
vừa_qua
vừa_rồi
vừa_vừa
à_này
à_ơi
ào_vào
ào_ào
á_à
âu_là
ít_biết
ít_có
ít_hơn
ít_khi
ít_lâu
ít_nhiều
ít_nhất
ít_nữa
ít_quá
ít_ra
ít_thôi
ít_thấy
ôi_chao
ôi_thôi
úi_chà
úi_dào
ơ_hay
ơ_kìa
ơi_là
ạ_ơi
ấy_là
ầu_ơ
ắt_hẳn
ắt_là
ắt_phải
ắt_thật
ối_dào
ối_giời
ối_giời_ơi
ồ_ồ
ớ_này
ờ_ờ
ở_lại
ở_như
ở_nhờ
ở_năm
ở_trên
ở_vào
ở_đây
ở_đó
ở_được
ứ_hự
ứ_ừ
ừ_nhé
ừ_thì
ừ_ào
ừ_ừ
""".split('\n'))
STOP_WORDS.remove('')

 # khai báo kí tự đặc biệt : 
SPEC_CHARS = set("""
'
…
"
-
`
_
.
♦
’
,
&
:
“
”
{
}
?
(
)
~
@
#
$
%
^
*
<
>
/
\\
!

=
+
•

[
]
0
1
2
3
4
5
6
7
8
9
©
–
¯
−
∗
θ
;
∈
×
∀
≤
≥
→


⇒
⇔
∃
ˆ
·
λ
|
α
∞
∇
∂







µ
σ
π
γ
β
≈
∝
≡
≺
∆
ε
""".split('\n'))
SPEC_CHARS.remove('')

# Define the connection parameters
params = urllib.parse.quote_plus(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=mssql-155580-0.cloudclusters.net,19084;'
    r'DATABASE=Group6_1;'
    r'UID=group6_1;'
    r'PWD=Group6123'
)

# Use the connection parameters in the connection string
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Define your list of product names
product_names = [
    "Áo bomber SST màu đỏ đô chất liệu Poly co giãn 4 chiều -Full tem, tag, mác đầy đủ - Phom dáng chuẩn phù hợp cả nam và nữ", 
    "Ốp Lưng trong Hỗ trợ hút sạc không dây vòng tròn từ tính cho iphone X/XS/XR/Xsmax/11/12/13/14/15/Plus/Pro/Max/Promax", 
    "Áo Polo Teelab Special chất cá sấu thoáng mát co dãn 4c , áo thun có cổ local brand nam nữ unisex form rộng", 
    "Áo khoác nam unisex cổ đứng vải dù 2 lớp phối màu độc lạ họa tiết chữ RESUAPRE đi mưa,cản gió,chống nắng",
    "Thắt lưng nam LV, dây lưng nam Caro đủ màu, đầu khóa chữ nhỏ A1CLV1",
    "Dây lưng nam cao cấp, thắt lưng nam lv, dây lưng lv thời trang, mặt kim loại nguyên khối trẻ trung lịch lãm TLLV002",
    "ĐỒ BỘ NAM THỂ THAO THUN COTTON-NLSAO",
    "Thắt Lưng Da Nam Khóa Tự Động Cao Cấp Dây Nịt Nam Mặt Xoay Chính Hãng , Phong Cách Hàn Quốc",
    "Ốp Điện Thoại Màu Kẹo Trơn Hình Gấu 3D Sang Trọng Cho iPhone 7 8 14 Plus XR 11 14 12 13 Pro MAX X XS MAX",
    "Áo khoác nam cổ trụ vải dù 2 lớp phong cách trường học hàn quốc họa tiết thêu chữ adapisl D62",
    "SẠC CỰC NHANH - PIN SẠC DỰ PHÒNG 30000MAH MẶT GƯƠNG ĐEN HUYỀN THOẠI",
    "Áo thun tay lỡ Sad Boy Nam Nữ chất Cotton oversize form rộng Four Basic"
]

# Set background color
set_bg_and_text_color()

# Create the option menu as a navigation bar
with st.sidebar:
    selected = option_menu(
        menu_title=None,  # This should be a string, but you can set it to None or "" if you don't want a title
        options=["HomePage", "Products", "Reviews"],
        icons=["house", "box", "star-fill"],
        menu_icon="cast",  # This should be a string, and it specifies the icon for the menu itself
        default_index=0,
        orientation="horizontal"
    )


if selected == "HomePage":
# title and insert picture 
    st.title("Experimental program conducted by group 6: Application of Sentiment Analysis")
    st.image("1.jpg")

    user_input = st.text_area("Enter your comment:", "")
    # trả về kết quả
    if st.button("Analyze"):
        if user_input:  # Kiểm tra nếu đầu vào không rỗng
            try:
                describe_result,quality_result, shipping_result = predict_sentiment(user_input)
                display_result_with_emoji("Describe Product Sentiment:", describe_result)  # Hiển thị kết quả từ model1
                display_result_with_emoji("Quality Product Sentiment:", quality_result)  # Hiển thị kết quả từ model2
                display_result_with_emoji("Shipping Product Sentiment:", shipping_result)  # Hiển thị kết quả từ model3
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
        else:
            st.error("Please enter some text to analyze.")

elif selected == "Products":
    # Perform database query
    product = st.selectbox("Choose a product", product_names)
    
    # Escape single quotes in the product name
    product_escaped = product.replace("'", "''")
    
    # Query the database for comments related to the selected product
    query = f"""
    SELECT [Mô tả sản phẩm], [Chất lượng sản phẩm], [Chất lượng vận chuyển]
    FROM Shopee
    WHERE [Tên sp] = N'{product_escaped}'
    """
    df = pd.read_sql_query(query, engine)
    
    # Replace the sentiment values with numerical values if needed
    sentiment_map = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    df = df.replace(sentiment_map)

    # Aggregate the comments by sentiment for each criterion
    describe_counts = df['Mô tả sản phẩm'].value_counts()
    quality_counts = df['Chất lượng sản phẩm'].value_counts()
    shipping_counts = df['Chất lượng vận chuyển'].value_counts()

    # Visualize with pie charts
    fig_describe = px.pie(values=describe_counts, names=describe_counts.index, title='Describe Product Sentiment')
    fig_quality = px.pie(values=quality_counts, names=quality_counts.index, title='Quality Product Sentiment')
    fig_shipping = px.pie(values=shipping_counts, names=shipping_counts.index, title='Shipping Product Sentiment')

    # Display the pie charts in Streamlit
    st.plotly_chart(fig_describe)
    st.plotly_chart(fig_quality)
    st.plotly_chart(fig_shipping)





