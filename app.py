import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from PIL import Image
from datetime import date
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TreeSense AI",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #f4f8f3;
}

/* Main headings */
h1, h2, h3 {
    color: #173f2a;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #123524 0%,
        #1b5e3a 100%
    );
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background-color: green;
    border: 1px solid #dce8df;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.05);
}

/* Buttons */
.stButton > button {
    background-color: #000000;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #164d32;
    color: white;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background-color: white;
    border-radius: 12px;
    padding: 10px;
}

/* General cards */
.tree-card {
    background-color: green;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #dce8df;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.04);
    margin-bottom: 15px;
}

.status-healthy {
    background-color: #000000;
    color: #176b36;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
}

.status-stressed {
    background-color: #000000;
    color: #9a6400;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
}

.status-diseased {
    background-color: #green;
    color: #a72a2a;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "tree_inventory" not in st.session_state:

    st.session_state.tree_inventory = pd.DataFrame(
        columns=[
            "Tree ID",
            "Species",
            "Health",
            "Leaf Colour",
            "Canopy Density",
            "Disease Symptoms",
            "Trunk Damage",
            "Pest Infestation",
            "Latitude",
            "Longitude",
            "Survey Date"
        ]
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🌳 TreeSense AI")

    st.caption(
        "Urban Tree Health Intelligence"
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📷 AI Tree Diagnosis",
            "📝 Tree Survey",
            "🌳 Tree Inventory",
            "🗺️ Health Map",
            "📊 Model Performance",
            "ℹ️ About"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.caption(
        "AI-Based Urban Tree Health Monitoring System"
    )

    st.caption(
        "UPES Campus Tree Survey"
    )


# =========================================================
# HEADER FUNCTION
# =========================================================

def page_header(title, subtitle):

    st.title(title)

    st.write(subtitle)

    st.markdown("---")


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    page_header(
        "🌳 TreeSense AI Dashboard",
        "Urban Tree Health Monitoring & Geospatial Intelligence Platform"
    )

    inventory = st.session_state.tree_inventory

    total_trees = len(inventory)

    if total_trees > 0:

        healthy = len(
            inventory[inventory["Health"] == "Healthy"]
        )

        stressed = len(
            inventory[
                inventory["Health"]
                == "Moderately Stressed"
            ]
        )

        diseased = len(
            inventory[
                inventory["Health"]
                == "Diseased / Damaged"
            ]
        )

    else:

        healthy = 0
        stressed = 0
        diseased = 0

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌳 Trees Surveyed",
        total_trees
    )

    col2.metric(
        "🟢 Healthy",
        healthy
    )

    col3.metric(
        "🟠 Moderately Stressed",
        stressed
    )

    col4.metric(
        "🔴 Diseased / Damaged",
        diseased
    )

    st.markdown("### Tree Health Overview")

    if total_trees == 0:

        st.info(
            "No tree surveys have been recorded yet. "
            "Open the Tree Survey section to add your first tree."
        )

    else:

        chart_data = pd.DataFrame({
            "Health Status": [
                "Healthy",
                "Moderately Stressed",
                "Diseased / Damaged"
            ],
            "Trees": [
                healthy,
                stressed,
                diseased
            ]
        })

        fig = px.pie(
            chart_data,
            values="Trees",
            names="Health Status",
            hole=0.55,
            title="Tree Health Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### 🌍 Survey Map")

    if total_trees == 0:

        # Approximate default campus-region view.
        # Replace with exact campus coordinates if required.
        map_center = [30.416, 77.968]

    else:

        map_center = [
            inventory["Latitude"].astype(float).mean(),
            inventory["Longitude"].astype(float).mean()
        ]

    dashboard_map = folium.Map(
        location=map_center,
        zoom_start=15,
        tiles="OpenStreetMap"
    )

    if total_trees > 0:

        for _, tree in inventory.iterrows():

            if tree["Health"] == "Healthy":
                marker_color = "green"

            elif tree["Health"] == "Moderately Stressed":
                marker_color = "orange"

            else:
                marker_color = "red"

            folium.Marker(
                location=[
                    float(tree["Latitude"]),
                    float(tree["Longitude"])
                ],
                popup=f"""
                <b>{tree['Tree ID']}</b><br>
                Species: {tree['Species']}<br>
                Health: {tree['Health']}<br>
                Canopy: {tree['Canopy Density']}
                """,
                icon=folium.Icon(
                    color=marker_color,
                    icon="tree",
                    prefix="fa"
                )
            ).add_to(dashboard_map)

    st_folium(
        dashboard_map,
        width=None,
        height=500
    )


# =========================================================
# AI TREE DIAGNOSIS
# =========================================================

elif page == "📷 AI Tree Diagnosis":

    page_header(
        "📷 AI Tree Diagnosis",
        "Upload a tree or leaf photograph for health assessment."
    )

    st.info(
        "The interface is ready for AI integration. "
        "Actual predictions will become available after the "
        "MobileNet/EfficientNet model has been trained."
    )

    col1, col2 = st.columns([1, 1])

    with col1:

        st.subheader("Upload Image")

        uploaded_image = st.file_uploader(
            "Tree or leaf photograph",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )

        if uploaded_image is not None:

            image = Image.open(uploaded_image)

            st.image(
                image,
                caption="Uploaded Tree Image",
                use_container_width=True
            )

    with col2:

        st.subheader("Tree Information")

        diagnosis_species = st.text_input(
            "Tree Species",
            placeholder="e.g. Neem"
        )

        diagnosis_leaf = st.selectbox(
            "Leaf Colour",
            [
                "Dark Green",
                "Light Green",
                "Yellow-Green",
                "Yellow",
                "Brown",
                "Mixed / Discoloured"
            ]
        )

        diagnosis_canopy = st.selectbox(
            "Canopy Density",
            [
                "Dense",
                "Moderate",
                "Sparse",
                "Severely Defoliated"
            ]
        )

        diagnosis_symptoms = st.multiselect(
            "Visible Symptoms",
            [
                "None",
                "Leaf Spots",
                "Yellowing",
                "Wilting",
                "Dieback",
                "Fungal Growth",
                "Leaf Loss",
                "Bark Damage",
                "Other"
            ]
        )

        if st.button(
            "🔍 Analyse Tree",
            use_container_width=True
        ):

            if uploaded_image is None:

                st.warning(
                    "Please upload a tree or leaf photograph."
                )

            else:

                st.warning(
                    "AI model not connected yet. "
                    "This photograph has been accepted successfully, "
                    "but a health prediction cannot be produced until "
                    "the trained model is integrated."
                )

                st.markdown("### Model Input")

                st.write(
                    f"**Species:** "
                    f"{diagnosis_species or 'Not specified'}"
                )

                st.write(
                    f"**Leaf Colour:** {diagnosis_leaf}"
                )

                st.write(
                    f"**Canopy Density:** {diagnosis_canopy}"
                )

                st.write(
                    "**Symptoms:** "
                    + (
                        ", ".join(diagnosis_symptoms)
                        if diagnosis_symptoms
                        else "None recorded"
                    )
                )


# =========================================================
# TREE SURVEY
# =========================================================

elif page == "📝 Tree Survey":

    page_header(
        "📝 Tree Survey",
        "Record field observations for individual trees."
    )

    with st.form("tree_survey_form"):

        col1, col2 = st.columns(2)

        with col1:

            tree_id = st.text_input(
                "Tree ID",
                placeholder="Example: UPES-001"
            )

            species = st.text_input(
                "Tree Species",
                placeholder="Example: Neem"
            )

            survey_date = st.date_input(
                "Survey Date",
                value=date.today()
            )

            leaf_colour = st.selectbox(
                "Leaf Colour",
                [
                    "Dark Green",
                    "Light Green",
                    "Yellow-Green",
                    "Yellow",
                    "Brown",
                    "Mixed / Discoloured"
                ]
            )

            canopy_density = st.selectbox(
                "Canopy Density",
                [
                    "Dense",
                    "Moderate",
                    "Sparse",
                    "Severely Defoliated"
                ]
            )

        with col2:

            health_status = st.selectbox(
                "Field-Assessed Health Status",
                [
                    "Healthy",
                    "Moderately Stressed",
                    "Diseased / Damaged"
                ]
            )

            disease_symptoms = st.multiselect(
                "Visible Disease Symptoms",
                [
                    "None",
                    "Leaf Spots",
                    "Yellowing",
                    "Wilting",
                    "Dieback",
                    "Fungal Growth",
                    "Leaf Loss",
                    "Other"
                ]
            )

            trunk_damage = st.selectbox(
                "Trunk Condition",
                [
                    "No Visible Damage",
                    "Minor Bark Damage",
                    "Cracks",
                    "Cavities",
                    "Major Structural Damage"
                ]
            )

            pest = st.selectbox(
                "Pest Infestation",
                [
                    "None",
                    "Mild",
                    "Moderate",
                    "Severe"
                ]
            )

        st.markdown("### 📍 GPS Location")

        gps1, gps2 = st.columns(2)

        with gps1:

            latitude = st.number_input(
                "Latitude",
                format="%.6f",
                value=30.416000
            )

        with gps2:

            longitude = st.number_input(
                "Longitude",
                format="%.6f",
                value=77.968000
            )

        st.markdown("### 📷 Tree Photograph")

        survey_image = st.file_uploader(
            "Upload photograph",
            type=[
                "jpg",
                "jpeg",
                "png"
            ],
            key="survey_photo"
        )

        notes = st.text_area(
            "Additional Field Notes",
            placeholder=(
                "Enter any additional observations..."
            )
        )

        submitted = st.form_submit_button(
            "💾 Save Tree Survey",
            use_container_width=True
        )

        if submitted:

            if tree_id.strip() == "":

                st.error(
                    "Please enter a Tree ID."
                )

            elif species.strip() == "":

                st.error(
                    "Please enter the tree species."
                )

            elif (
                tree_id
                in st.session_state.tree_inventory[
                    "Tree ID"
                ].values
            ):

                st.error(
                    "This Tree ID already exists."
                )

            else:

                new_tree = pd.DataFrame([{
                    "Tree ID": tree_id,
                    "Species": species,
                    "Health": health_status,
                    "Leaf Colour": leaf_colour,
                    "Canopy Density": canopy_density,
                    "Disease Symptoms":
                        ", ".join(disease_symptoms)
                        if disease_symptoms
                        else "None",
                    "Trunk Damage": trunk_damage,
                    "Pest Infestation": pest,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Survey Date": str(survey_date)
                }])

                st.session_state.tree_inventory = (
                    pd.concat(
                        [
                            st.session_state.tree_inventory,
                            new_tree
                        ],
                        ignore_index=True
                    )
                )

                st.success(
                    f"Tree {tree_id} has been added "
                    "to the inventory."
                )


# =========================================================
# TREE INVENTORY
# =========================================================


    page_header(
        "🌳 Tree Inventory",
        "View and manage surveyed urban trees."
    )

    inventory = st.session_state.tree_inventory

    if len(inventory) == 0:

        st.info(
            "The tree inventory is currently empty."
        )

    else:

        col1, col2 = st.columns([2, 1])

        with col1:

            search = st.text_input(
                "🔎 Search inventory",
                placeholder="Tree ID or species"
            )

        with col2:

            filter_health = st.selectbox(
                "Health Filter",
                [
                    "All",
                    "Healthy",
                    "Moderately Stressed",
                    "Diseased / Damaged"
                ]
            )

        filtered = inventory.copy()

        if search:

            filtered = filtered[
                filtered["Tree ID"].str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                filtered["Species"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if filter_health != "All":

            filtered = filtered[
                filtered["Health"] == filter_health
            ]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        csv = inventory.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Tree Inventory",
            data=csv,
            file_name="treesense_tree_inventory.csv",
            mime="text/csv"
        )


# =========================================================
# HEALTH MAP
# =========================================================

elif page == "🗺️ Health Map":

    page_header(
        "🗺️ Tree Health Map",
        "Geospatial visualisation of surveyed tree health."
    )

    inventory = st.session_state.tree_inventory

    if len(inventory) == 0:

        st.warning(
            "No surveyed trees are available for mapping."
        )

        health_map = folium.Map(
            location=[30.416, 77.968],
            zoom_start=15
        )

    else:

        map_lat = inventory[
            "Latitude"
        ].astype(float).mean()

        map_lon = inventory[
            "Longitude"
        ].astype(float).mean()

        health_map = folium.Map(
            location=[
                map_lat,
                map_lon
            ],
            zoom_start=16
        )

        for _, tree in inventory.iterrows():

            if tree["Health"] == "Healthy":

                colour = "green"

            elif (
                tree["Health"]
                == "Moderately Stressed"
            ):

                colour = "orange"

            else:

                colour = "red"

            popup = f"""
            <b>Tree ID:</b> {tree['Tree ID']}<br>
            <b>Species:</b> {tree['Species']}<br>
            <b>Health:</b> {tree['Health']}<br>
            <b>Leaf Colour:</b> {tree['Leaf Colour']}<br>
            <b>Canopy:</b> {tree['Canopy Density']}<br>
            <b>Pests:</b> {tree['Pest Infestation']}<br>
            <b>Survey:</b> {tree['Survey Date']}
            """

            folium.Marker(
                [
                    float(tree["Latitude"]),
                    float(tree["Longitude"])
                ],
                popup=folium.Popup(
                    popup,
                    max_width=300
                ),
                tooltip=tree["Tree ID"],
                icon=folium.Icon(
                    color=colour,
                    icon="tree",
                    prefix="fa"
                )
            ).add_to(health_map)

    st_folium(
        health_map,
        width=None,
        height=600
    )

    st.markdown(
        """
        **Map Legend**

        🟢 Healthy  
        🟠 Moderately Stressed  
        🔴 Diseased / Damaged
        """
    )


# =========================================================
# MODEL PERFORMANCE
# =========================================================

elif page == "📊 Model Performance":

    page_header(
        "📊 AI Model Performance",
        "Performance evaluation of the tree-health "
        "classification model."
    )

    st.warning(
        "No trained AI model has been connected yet."
    )

    st.markdown("### Planned Model")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Architecture",
        "MobileNetV2"
    )

    col2.metric(
        "Classes",
        "3"
    )

    col3.metric(
        "Model Status",
        "Not Trained"
    )

    st.markdown("### Classification Classes")

    st.success(
        "🟢 Healthy"
    )

    st.warning(
        "🟠 Moderately Stressed"
    )

    st.error(
        "🔴 Diseased / Damaged"
    )

    st.markdown("### Evaluation Metrics")

    st.write(
        """
        After model training, this page will display:

        - Training accuracy
        - Validation accuracy
        - Test accuracy
        - Training and validation loss
        - Confusion matrix
        - Precision
        - Recall
        - F1-score
        - Class-wise prediction performance
        """
    )


# =========================================================
# ABOUT
# =========================================================

elif page == "ℹ️ About":

    page_header(
        "ℹ️ About TreeSense AI",
        "AI-Based Urban Tree Health Monitoring System"
    )

    st.markdown(
        """
        ### Project Objective

        **TreeSense AI** is designed to support urban tree-health
        surveys by combining field observations, artificial
        intelligence and geospatial mapping.

        The initial implementation is intended for tree-health
        assessment on the **UPES campus**.

        ### Health Classification

        Trees are classified into three categories:

        **🟢 Healthy**  
        Trees showing normal foliage, canopy development and
        no significant visible damage.

        **🟠 Moderately Stressed**  
        Trees showing signs such as reduced canopy density,
        yellowing, minor pest infestation or early disease
        symptoms.

        **🔴 Diseased / Damaged**  
        Trees showing significant disease, pest infestation,
        structural damage, severe defoliation or decline.

        ### Data Inputs

        The system incorporates:

        - Tree and leaf photographs
        - Tree species
        - Leaf colour
        - Canopy density
        - Visible disease symptoms
        - Trunk condition
        - Pest infestation
        - GPS coordinates
        - Survey date

        ### Artificial Intelligence

        The planned image-classification model will use
        **transfer learning**, initially with **MobileNetV2**.

        The model will be trained using labelled photographs
        belonging to the three tree-health classes.

        ### Expected Outputs

        - Tree-health classification
        - AI prediction confidence
        - Model accuracy
        - Digital tree inventory
        - Interactive health-status map
        - Survey statistics
        - Model-performance visualisations
        """
    )

    st.markdown("---")

    st.caption(
        "TreeSense AI • Urban Tree Health Intelligence"
    )
