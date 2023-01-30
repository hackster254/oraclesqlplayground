import streamlit as st
import pandas as pd
import cx_Oracle
 


# connect db
connection = cx_Oracle.connect(user='hr', password='hr', dsn='localhost/xepdb1')
cursor = connection.cursor()

# function to run the sql code on oracledb
def sql_executor(raw_code):
    cursor.execute(raw_code)
    print('raw code passed is '+raw_code)
    data = cursor.fetchall()
 
    return data


def main():
    st.title('Oracle Playground')

    menu = ['Home','About']
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader('HomePage')

        # columns
        col1,col2 = st.columns(2)

        with col1:
            with st.form(key='query_form'):
                raw_code = st.text_area('Type SQL code here')
                submit_code = st.form_submit_button('Execute sql')

            #table of info about all the tables in the db
            with st.expander('Table info'):
                st.write(sql_executor("SELECT table_name FROM   ALL_tables WHERE  owner = 'HR'"))
        
        # show results
        with col2:
            if submit_code:
                st.info('Query submited')
                st.code(raw_code)

                # results
                query_results = sql_executor(raw_code)
                st.write(raw_code)
                with st.expander("Results"):
                    st.write(query_results)
                
                with st.expander('Tablelized'):
                    query_table = pd.DataFrame(query_results)
                    st.dataframe(query_table)
    else:
        st.subheader('About')


if __name__ == '__main__':
    main()