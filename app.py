
                st.success("Tree survey saved to the inventory.")
                st.rerun()


# ---------------------------------------------------------
# TREE INVENTORY
# ---------------------------------------------------------
elif page == "Tree Inventory":
    st.title("📋 Tree Inventory")
    inventory = load_inventory()

    if inventory.empty:
        st.info("No tree records are available yet. Add a survey using Tree Health Prediction.")
    else:
        st.metric("Total records", len(inventory))
        st.dataframe(inventory, use_container_width=True, hide_index=True)

        csv_data = inventory.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Tree Inventory (CSV)",
            data=csv_data,
            file_name="tree_inventory.csv",
            mime="text/csv",
        )

        record_to_delete = st.text_input("Enter Tree ID to delete a record")
        if st.button("Delete Tree Record"):
            updated = inventory[inventory["Tree ID"].astype(str) != record_to_delete.strip()]
            if len(updated) == len(inventory):
                st.warning("No matching Tree ID was found.")
            else:
                save_inventory(updated)
                st.success("Record deleted.")
                st.rerun()


# ---------------------------------------------------------
# HEALTH STATUS MAP
# ---------------------------------------------------------
elif page == "Health Status Map":
    st.title("🗺️ Tree Health Status Map")
    inventory = load_inventory()

    if inventory.empty or not inventory[["Latitude", "Longitude"]].notna().all(axis=1).any():
        st.info("No geotagged tree records are available yet.")
    elif folium is None or st_folium is None:
        st.warning("Map packages are not installed. Install folium and streamlit-folium.")
    else:
        map_data = inventory.dropna(subset=["Latitude", "Longitude"]).copy()
        center = [
            float(map_data["Latitude"].mean()),
            float(map_data["Longitude"].mean()),
        ]
        tree_map = folium.Map(location=center, zoom_start=16, tiles="OpenStreetMap")

        for _, row in map_data.iterrows():
            status = str(row["Health Status"])
            color = (
                "green" if status == "Healthy"
                else "orange" if status == "Moderately Stressed"
                else "red"
            )
            popup_text = (
                f"Tree ID: {row['Tree ID']}<br>"
                f"Species: {row['Species']}<br>"
                f"Health: {status}"
            )
            folium.Marker(
                location=[float(row["Latitude"]), float(row["Longitude"])],
                popup=folium.Popup(popup_text, max_width=250),
                tooltip=str(row["Tree ID"]),
                icon=folium.Icon(color=color, icon="tree", prefix="fa"),
            ).add_to(tree_map)

        st_folium(tree_map, width=None, height=560, use_container_width=True)
        st.caption("Green = Healthy | Orange = Moderately Stressed | Red = Diseased / Damaged")


# ---------------------------------------------------------
# MODEL EVALUATION
# ---------------------------------------------------------
elif page == "Model Evaluation":
    st.title("📊 Model Evaluation")

    history_data = st.session_state.get("training_history")
    if history_data:
        st.subheader("Training performance")
        accuracy_df = pd.DataFrame({
            "Epoch": range(1, len(history_data["accuracy"]) + 1),
            "Training accuracy": history_data["accuracy"],
            "Validation accuracy": history_data["val_accuracy"],
        }).set_index("Epoch")
        st.line_chart(accuracy_df)

        loss_df = pd.DataFrame({
            "Epoch": range(1, len(history_data["loss"]) + 1),
            "Training loss": history_data["loss"],
            "Validation loss": history_data["val_loss"],
        }).set_index("Epoch")
        st.line_chart(loss_df)

        st.write(f"Final training accuracy: **{history_data['accuracy'][-1] * 100:.2f}%**")
        st.write(f"Final validation accuracy: **{history_data['val_accuracy'][-1] * 100:.2f}%**")
    else:
        st.info(
            "Training graphs will appear here after you train the model in this session. "
            "The saved model can still be used for predictions."
        )

    inventory = load_inventory()
    if not inventory.empty:
        st.subheader("Survey summary")
        counts = inventory["Health Status"].value_counts().reindex(CLASS_NAMES, fill_value=0)
        st.bar_chart(counts)
    else:
        st.info("Add tree surveys to view the health-status summary.")
