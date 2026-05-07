from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from agent.orchestrator import AutonomousLabOrchestrator


st.set_page_config(page_title="Project Catalyst - Autonomous Lab", layout="wide")
st.title("Project Catalyst: Autonomous Lab")

query = st.text_area(
    "Research query",
    value="Analyze this CSV of seismic data and predict the next trend.",
    height=100,
)

sovereignty_toggle = st.toggle("Sovereignty Toggle (Zero External API Calls)", value=True)

if st.button("Run Think-Code-Verify"):
    orchestrator = AutonomousLabOrchestrator(output_directory=Path("output"))
    result = orchestrator.run(query)

    terminal_col, artifact_col = st.columns([2, 1])

    with terminal_col:
        st.subheader("Terminal View")
        monologue = [result.planner_thought]
        monologue.extend(step.reflection for step in result.steps if step.reflection)
        st.code("\n".join(monologue) or "No internal monologue recorded.", language="text")

        for step in result.steps:
            st.markdown(f"**Step {step.step_id}: {step.objective}**")
            st.code(step.stdout or step.stderr or "(No output)", language="text")

    with artifact_col:
        st.subheader("Artifact Gallery")
        output_dir = result.output_directory
        image_paths = sorted(output_dir.glob("*.png")) + sorted(output_dir.glob("*.jpg"))
        csv_paths = sorted(output_dir.glob("*.csv"))

        if not image_paths and not csv_paths:
            st.info("No artifacts were generated yet.")

        for image in image_paths:
            st.image(str(image), caption=image.name, use_container_width=True)

        for csv_file in csv_paths:
            st.markdown(f"**{csv_file.name}**")
            st.dataframe(pd.read_csv(csv_file))

    if sovereignty_toggle:
        verified = result.external_api_attempts == 0
        st.success(f"Zero External API Calls: {'Verified' if verified else 'Not Verified'}")
        st.caption(f"Observed network connection attempts: {result.external_api_attempts}")
