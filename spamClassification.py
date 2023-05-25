import pickle
import streamlit as st
import win32com.client
import pandas as pd
from st_aggrid import AgGrid

model = pickle.load(open("spam.pkl", "rb"))
cv = pickle.load(open("vectorizer.pkl", "rb"))

def main():
    outlook = win32com.client.Dispatch('Outlook.Application')
    mapi = outlook.GetNamespace("MAPI")
    st.title("Phận biệt mail spam")
    st.subheader("Nhập email")
    email = st.text_input("Nhập email:")
    if st.button("Phân loại"):
        subj = []
        body = []
        decti = []
        your_folder = mapi.Folders[str(email)].Folders['Inbox']
        messages = your_folder.Items
        for item in messages:
            subj.append(item.Subject)
            body.append(item.body)
            a = item.Subject + " " + item.body
            dataa = [a]
            vect = cv.transform(dataa).toarray()
            prediction = model.predict(vect)
            if prediction[0] == 1:
                decti.append("Spam")
            if prediction[0] == 0:
                decti.append("Ham")

        d = {'Classification': decti, 'Subject': subj, 'Content': body}
        df = pd.DataFrame(data=d)
        st.subheader("Email Spam")
        st.dataframe(df[df.Classification == "Spam"])
        st.subheader("Email Không Spam")
        st.dataframe(df[df.Classification == "Ham"])

    #st.subheader("Nhập nội dung ")
    #msg = st.text_input("Nhập content:")
    #if st.button("Predict"):
        #data = [msg]
        #vect = cv.transform(data).toarray()
        #prediction = model.predict(vect)
        #st.success(prediction[0])
main()
