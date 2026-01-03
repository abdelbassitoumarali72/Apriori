import streamlit as st

import pandas as pd


from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

st.sidebar.title("⚙️ Paramètres")
min_sup = st.sidebar.slider("Support minimum",0.001,0.1,0.001)
min_conf  = st.sidebar.slider("Confiance minimum", 0.1, 1.0, 0.7)
min_lift = st.sidebar.slider("lift minimum",0.1,2.0,1.25)

st.title("🏠 APRIORI")

# Titre de l'application
st.header("🛒 Analyser le panier de la clientèle") # grand titr

data_type=st.selectbox( "  CHOISISSEZ LE FORMAT DE DOCUMENT ",["","csv","excel"])

data = st.file_uploader("REJOINDRE LE DOCUMENT 📂", type=["csv","xlsx", "xls"])
    
if data is not None:
    extension = data.name.split(".")[-1].lower()
                
    if data_type== "csv" and extension == "csv":
        dataset = pd.read_csv(data, header=None)
        #limite=st.radio("délimiteur",[",",";"])
    
        dataset = (
        dataset
        .apply(lambda row: [
            str(item).strip()
            for item in row
            if pd.notna(item) and str(item).strip() != ""
        ], axis=1)
        .tolist()
        )

    
        #df = dataset.values.tolist()
    
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns = te.columns_)
     
        #min_sup_auto = 1 / len(dataset)
    
        # Extraire les itemsets fréquents avec un support minimum de 0.4
        frequent_itemsets = apriori(df, min_support = min_sup, use_colnames = True)
    
        # on filtre par confidence au moins 0.7
        rules_confiance = association_rules(frequent_itemsets, metric = "confidence", min_threshold  = min_conf)
    
        #On peut aussi filtrer par lift
        rules_lift = association_rules(frequent_itemsets, metric = "lift", min_threshold = min_lift)
    
        choix=st.selectbox("Sélectionner",["","rules_lift","rules_confiance"])
        if choix=="rules_lift":   
            st.write("Support :", rules_lift)
           
    
        elif choix=="rules_confiance":
            st.write(rules_confiance)
            ##fig, ax = plt.subplots()
        
            #ax.set_xlabel("Support")
            #ax.set_ylabel("Confiance")
            #ax.set_title("Support vs Confiance")
            
            #st.pyplot(fig)

############################################################################################################
    
    elif data_type== "excel" and extension in ["xlsx", "xls"]:
        
        dataset = pd.read_excel(data, header=None)

        transactions = []

        for _, row in dataset.iterrows():
            transaction = [
            str(item).strip()
            for item in row
            if pd.notna(item) and str(item).strip() != ""
            ]
            transactions.append(transaction)

        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns = te.columns_)

         
        
       # Extraire les itemsets fréquents avec un support minimum de 0.4
        frequent_itemsets = apriori(df, min_support = min_sup, use_colnames = True)

        # on filtre par confidence au moins 0.7
        rules_confiance = association_rules(frequent_itemsets, metric = "confidence", min_threshold  = min_conf)

        #rules_confiance = rules_confiance[(rules_confiance["confidence"] >= min_conf) & (rules_confiance["lift"] >= min_lift)]

        
        #On peut aussi filtrer par lift
        rules_lift = association_rules(frequent_itemsets, metric = "lift", min_threshold = min_lift)

        choix=st.selectbox("Sélectionner",["","rules_lift","rules_confiance"])
        if choix=="rules_lift":   
            st.write("Support :", rules_lift)
         

        elif choix=="rules_confiance":
            st.write(rules_confiance)
            


    elif data_type == "csv" and extension != "csv":
        st.error("❌ Vous avez sélectionné CSV mais importé un fichier Excel")

    elif data_type == "excel" and extension not in ["xls", "xlsx"]:
        st.error("❌ Vous avez sélectionné Excel mais importé un fichier CSV")
