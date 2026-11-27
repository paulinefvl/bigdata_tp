import pandas as pd
import plotly.express as px
import streamlit as st

# Je charge mes deux fichiers Parquet pseudonymisés
commandes = pd.read_parquet("data/commandes_pseudo.parquet")
paiements = pd.read_parquet("data/paiements_pseudo.parquet")

# Je garde seulement les paiements acceptés pour les encaissements
paid = paiements[paiements["payment_status"] == "PAID"]

# Le menu sur le côté pour changer de page
st.sidebar.title("BigData Commerce Analytics")
page = st.sidebar.radio("Menu", ["Accueil", "Catégories", "Mois", "Clients", "Paiements", "Données"])

# Page d'accueil avec mes 4 chiffres clés
if page == "Accueil":
    st.title("Vue d'ensemble")
    st.metric("CA des commandes", round(commandes["discounted_line_total"].sum()))
    st.metric("Encaissements (PAID)", round(paid["amount"].sum()))
    st.metric("Nombre de paniers", len(paiements))
    st.metric("Taux de paiements acceptés", f"{len(paid) / len(paiements) * 100:.1f} %")

# Le CA par catégorie en barres horizontales
if page == "Catégories":
    st.title("Chiffre d'affaires par catégorie")
    ca = commandes.groupby("category")["discounted_line_total"].sum().sort_values()
    fig = px.bar(x=ca.values, y=ca.index, orientation="h", labels={"x": "CA", "y": "Catégorie"})
    st.plotly_chart(fig)

# La courbe des encaissements par mois
if page == "Mois":
    st.title("Évolution mensuelle des encaissements")
    mois = paid["payment_date"].dt.strftime("%Y-%m")
    mensuel = paid.groupby(mois)["amount"].sum()
    fig = px.line(x=mensuel.index, y=mensuel.values, markers=True, labels={"x": "Mois", "y": "Montant encaissé"})
    st.plotly_chart(fig)
    st.warning("Attention : les dates sont inventées, la baisse n'est pas une vraie tendance.")

# Les 10 clients qui ont le plus payé (j'affiche juste le début du pseudonyme)
if page == "Clients":
    st.title("Top 10 des clients pseudonymisés")
    top10 = paid.groupby("user_id_pseudo")["amount"].sum().nlargest(10).sort_values()
    fig = px.bar(x=top10.values, y=top10.index.str[:10], orientation="h", labels={"x": "Montant payé", "y": "Client"})
    st.plotly_chart(fig)

# La répartition des statuts de paiement
if page == "Paiements":
    st.title("Statuts de paiement")
    statuts = paiements["payment_status"].value_counts()
    fig = px.pie(names=statuts.index, values=statuts.values)
    st.plotly_chart(fig)

# Le tableau des données pour explorer
if page == "Données":
    st.title("Exploration des données")
    st.dataframe(commandes)