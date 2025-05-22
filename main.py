import streamlit as st
import pandas as pd
from PIL import Image
import random
import sqlite3


conn = sqlite3.connect("drug_data.db")
c = conn.cursor()

def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table create Successfully')

def customer_add_data(Cname,Cpass, Cemail, Cstate,Cnumber):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_State, C_Number) VALUES(?,?,?,?,?)''', (Cname,Cpass,  Cemail, Cstate,Cnumber))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data
def customer_update(Cemail,Cnumber):
    c.execute(''' UPDATE Customers SET C_Number = ? WHERE C_Email = ?''', (Cnumber,Cemail,))
    conn.commit()
    print("Updating")
def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
    conn.commit()

def drug_update(Duse, Did):
    c.execute(''' UPDATE Drugs SET D_Use = ? WHERE D_id = ?''', (Duse,Did))
    conn.commit()
def drug_delete(Did):
    c.execute(''' DELETE FROM Drugs WHERE D_id = ?''', (Did,))
    conn.commit()

def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL, 
                D_id INT PRIMARY KEY NOT NULL)
                ''')
    print('DRUG Table create Successfully')

def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did):
    c.execute('''INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_id) VALUES(?,?,?,?,?)''', (Dname, Dexpdate, Duse, Dqty, Did))
    conn.commit()

def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data

def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL)
    ''')

def order_delete(Oid):
    c.execute(''' DELETE FROM Orders WHERE O_id = ?''', (Oid,))
    conn.commit()

def order_add_data(O_Name,O_Items,O_Qty,O_id):
    c.execute('''INSERT INTO Orders (O_Name, O_Items,O_Qty, O_id) VALUES(?,?,?,?)''',
              (O_Name,O_Items,O_Qty,O_id))
    conn.commit()


def order_view_data(customername):
    c.execute('SELECT * FROM ORDERS Where O_Name == ?',(customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM ORDERS')
    order_all_data = c.fetchall()
    return order_all_data

# def archive_create_table():
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS archive(
#                 O_Name VARCHAR(100) NOT NULL,
#                 O_Items VARCHAR(100) NOT NULL,
#                 O_Qty VARCHAR(100) NOT NULL,
#                 O_id VARCHAR(100) PRIMARY KEY NOT NULL)
#     ''')

# def archive_add_data(O_Name,O_Items,O_Qty,O_id):
#     c.execute('''INSERT INTO archive (O_Name, O_Items,O_Qty, O_id) VALUES(?,?,?,?)''',
#               (O_Name,O_Items,O_Qty,O_id))
#     conn.commit()


# def archive_view_data(customername):
#     c.execute('SELECT * FROM archive Where O_Name == ?',(customername,))
#     order_data = c.fetchall()
#     return order_data

# def archive_view_all_data():
#     c.execute('SELECT * FROM archive')
#     order_all_data = c.fetchall()
#     return order_all_data

def admin():
    st.title("Pharmacy Database Dashboard")
    menu = ["Drugs", "Customers", "Orders", "About"]
    choice = st.sidebar.selectbox("Menu", menu)


    if choice == "Drugs":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_area("When to Use")
            with col2:
                drug_quantity = st.text_area("Enter the quantity")
                drug_id = st.text_area("Enter the Drug id (example:#D1)")

            if st.button("Add Drug"):
                drug_add_data(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(drug_clean_df)
            with st.expander("View Drug Quantity"):
                drug_name_quantity_df = drug_clean_df[['Name','Quantity']]
                st.dataframe(drug_name_quantity_df)
        if choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_area("Drug ID")
            d_use = st.text_area("Drug Use")
            if st.button(label='Update'):
                drug_update(d_use,d_id)

        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_area("Drug ID")
            if st.button(label="Delete"):
                drug_delete(did)


    elif choice == "Customers":

        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password","Email-ID" ,"Area", "Number"])
                st.dataframe(cust_clean_df)

        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email,cust_number)

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)

    elif choice == "Orders":
       
        menu = ["View",'Execute']
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID"])
                st.dataframe(order_clean_df)
        if choice == 'Execute':
            st.subheader("Order Details")
            order_result = order_view_all_data()
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID"])
                st.dataframe(order_clean_df)
            st.subheader("Execute Order")
            Oid = st.text_area("OrderID")
            if st.button(label="Execute"):
                order_delete(Oid)
            if st.button(label="Cancel"):
                order_delete(Oid)

    # elif choice == "archive":

    #     menu = ["View"]
    #     choice = st.sidebar.selectbox("Menu", menu)
    #     if choice == "View":
    #         st.subheader("Order Details")
    #         order_result = archive_view_all_data()
    #         with st.expander("View All Order Data"):
    #             order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID"])
    #             st.dataframe(order_clean_df)

    elif choice == "About":
        st.subheader("DBMS Mini Project")
        st.subheader("By M M Sreenivishal(1BI22IC035),T N Mithun(1BI22IC039)")


def getauthenicate(username, password):
    print("Auth")
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?', (username,))
    cust_password = c.fetchall()
    print(password, "Parameter password")
    if cust_password[0][0] == password:
        print("Inside password")
        return True
    else:
        return False


def customer(username, password):
    try:
        if getauthenicate(username, password):
            print("In Customer")
            st.title("Welcome to Pharmacy Store")

            # st.subheader("Your Order Details")
            # order_result = order_view_data(username)
            # with st.expander("View All Order Data"):
            #     order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
            #     st.dataframe(order_clean_df)

            drug_result = drug_view_all_data()
            print(drug_result)
            count = 0


            # st.subheader("Drug: "+drug_result[0][0])
            # st.subheader("DOLO 650😷 (Rs 15)")
            # dolo650 = st.slider(label="Quantity",min_value=0, max_value=5, key= 1)
            # st.info("When to USE: " + str(drug_result[0][2]))


            st.subheader("Drug: " + drug_result[0][0])
            st.subheader('STEPCILS💊 (Rs 10)')
            strepsils = st.slider(label="Quantity",min_value=0, max_value=5, key= 2)
            st.info("When to USE: " + str(drug_result[0][2]))

            st.subheader("Drug: " + drug_result[1][0])
            st.subheader("VICKS🍬 (Rs 65)")
            vicks = st.slider(label="Quantity",min_value=0, max_value=5, key=3)
            st.info("When to USE: " + str(drug_result[1][2]))

            st.subheader("Drug: " + drug_result[2][0])
            st.subheader("Calpol☘️ (Rs 95)")
            Calpol = st.slider(label="Quantity",min_value=0, max_value=5, key=4)
            st.info("When to USE: " + str(drug_result[2][2]))

            st.subheader("Drug: " + drug_result[3][0])
            st.subheader("PanD☁️ (Rs 85)")
            PanD = st.slider(label="Quantity",min_value=0, max_value=5, key=5)
            st.info("When to USE: " + str(drug_result[3][2]))



            if st.button(label="Buy now 🛒"):
                O_items = ""

                # if int(dolo650) > 0:
                #     O_items += "Dolo-650,"
                if int(strepsils) > 0:
                    O_items += "Strepsils,"
                if int(vicks) > 0:
                    O_items += "Vicks"
                if int(Calpol-650) > 0:
                    O_items += "Calpol-650"
                if int(PanD) > 0:
                    O_items += "PanD"
                O_Qty = str(',') + str(strepsils) + str(",") + str(vicks) + str(",") + str(Calpol)+ str(",") + str(PanD)

                O_id = username + "#O" + str(random.randint(0, 100))
                count += 1
                if  not int(strepsils) and not int(vicks) and not int(Calpol) and not int(PanD):
                    st.error("Add Something")
                else:
                    st.success("Order added")
                order_add_data(username, O_items, O_Qty, O_id)
                
    except IndexError:
        st.error("Invalid username or password")









if __name__ == '__main__':
    drug_create_table()
    cust_create_table()
    order_create_table()

    header = st.container()
    header.title("PHARMARCY 💊")
    menu = ["Login", "SignUp","Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            customer(username, password)

    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_area("Email ID")
        with col2:
            cust_area = st.text_area("State")
        with col3:
            cust_number = st.text_area("Phone Number")

        if st.button("Signup"):
            if (cust_password == cust_password1):
                if not cust_name or not cust_email:
                    st.error("Invalid E-mail or Name")
                elif(len(cust_number)!=10):
                    st.error("Ph No should be 10 digit long")
                
                else:
                    customer_add_data(cust_name,cust_password,cust_email, cust_area, cust_number,)
                    st.success("Account Created!")
                    st.info("Go to Login Menu to login")
            else:
                st.warning('Password dont match')
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if username == 'admin' and password == 'admin':
            admin()





