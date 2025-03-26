import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Planning Gantt Interactif", layout="wide")
st.title("📅 Planning Gantt interactif avec édition")

uploaded_file = st.file_uploader("📥 Importer un fichier Excel de planning", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Convertir en datetime pour les colonnes de dates
    df["Début"] = pd.to_datetime(df["Début"])
    df["Fin"] = pd.to_datetime(df["Fin"])

    st.subheader("📝 Édition du planning")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MANUAL,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        height=300,
        theme="material"
    )

    edited_df = grid_response["data"]

    st.subheader("📊 Vue Gantt")
    fig = px.timeline(
        edited_df,
        x_start="Début",
        x_end="Fin",
        y="Poste",
        color="Priorité",
        hover_name="OF"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    # ✅ Export du planning modifié
    st.subheader("💾 Exporter le planning modifié")
    to_download = edited_df.copy()
    to_download["Début"] = to_download["Début"].dt.strftime('%Y-%m-%d')
    to_download["Fin"] = to_download["Fin"].dt.strftime('%Y-%m-%d')

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        to_download.to_excel(writer, index=False, sheet_name="Planning")

    st.download_button(
        label="📤 Télécharger le fichier modifié",
        data=output.getvalue(),
        file_name="planning_modifié.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("💡 Charge un fichier Excel pour afficher et éditer ton planning.")
