import sklearn

#from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

import streamlit as st
import pickle
import numpy as np

import base64
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return
set_png_as_page_bg('6.JPG')


classifier_name=['XGBoost', 'Гадание на кофейной гуще']
option = st.sidebar.selectbox('Евгений Викторович, какой алгоритм запустить?', classifier_name)
st.subheader(option)



#Importing model and label encoders
model=pickle.load(open("final_xg_model.pkl","rb"))
#model_1 = pickle.load(open("final_rf_model.pkl","rb"))
le_pik=pickle.load(open("label_encoding_for_gender.pkl","rb"))
le1_pik=pickle.load(open("label_encoding_for_geo.pkl","rb"))


def predict_churn(CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary):
    input = np.array([[CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary]]).astype(np.float64)
    if option == 'XGBoost':
        prediction = model.predict_proba(input)
        pred = '{0:.{1}f}'.format(prediction[0][0], 2)

    else:
        pred=0.30
        #st.markdown('Наверное, клиент останется в банке, но это не точно да и вообще надо звонить в Битву экстрасенсов.')

    return float(pred)


def main():
    st.title("Прогноз оттока клиентов")
    html_temp = """
    <div style="background-color:white ;padding:10px">
    <h2 style="color:red;text-align:center;">Заполни форму</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)





    st.sidebar.subheader("Приложение создано для курса Diving into Darkness of Data Science")
    st.sidebar.text("Разработчик - Братковский Е.В.")


    CreditScore = st.slider('Скоринговый балл', 300, 900)

    Geography = st.selectbox('География/регион', ['France', 'Germany', 'Spain'])
    Geo = int(le1_pik.transform([Geography]))

    Gender = st.selectbox('Пол', ['Male', 'Female'])
    Gen = int(le_pik.transform([Gender]))

    Age = st.slider("Возраст", 10, 95)

    Tenure = st.selectbox("Стаж", ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','10', '11', '12', '13', '14', '15'])

    Balance = st.slider("Баланс", 0.00, 250000.00)

    NumOfProducts = st.selectbox('Количество продуктов', ['1', '2', '3', '4'])

    HasCrCard = st.selectbox("Есть кредитная БПК ?", ['0', '1'])

    IsActiveMember = st.selectbox("Активный клиент ?", ['0', '1'])

    EstimatedSalary = st.slider("Зарплата", 0.00, 200000.00)

    churn_html = """  
              <div style="background-color:#f44336;padding:20px >
               <h2 style="color:red;text-align:center;"> Жаль, но теряем клиента.</h2>
               </div>
            """
    no_churn_html = """  
              <div style="background-color:#94be8d;padding:20px >
               <h2 style="color:green ;text-align:center;"> Ура, клиент остаётся в банке !!!</h2>
               </div>
            """

    if st.button('Сделать прогноз'):
        output = predict_churn(CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
        st.success('Вероятность оттока составляет {}'.format(output))
        st.balloons()

        if output >= 0.5:
            st.markdown(churn_html, unsafe_allow_html= True)

        else:
            st.markdown(no_churn_html, unsafe_allow_html= True)

if __name__=='__main__':
    main()
