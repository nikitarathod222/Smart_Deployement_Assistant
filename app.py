from pathlib import Path
import time

import streamlit as st

from ai_helper import generate_dockerfile

st.set_page_config(
    page_title="Smart Deployment Assistant",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "docker_result" not in st.session_state:
    st.session_state.docker_result = None
if "deploy_url" not in st.session_state:
    st.session_state.deploy_url = None
if "last_status" not in st.session_state:
    st.session_state.last_status = None

css_path = Path(__file__).parent / "static" / "streamlit.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_metric_card(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <strong>{title}</strong>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_panel_heading(kicker: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="section-heading">
            <div class="small-kicker">{kicker}</div>
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def login() -> None:
    left_col, right_col = st.columns([1.15, 0.85], gap="large")

    with left_col:
        st.markdown(
            """
            <section class="hero-banner">
                <span class="eyebrow">Deployment workspace</span>
                <h1>Generate Docker-ready releases with a cleaner workflow.</h1>
                <p>Use Smart Deployment Assistant to review project context, generate a Dockerfile, download the output, and hand off a preview deployment from one structured workspace.</p>
                <div class="chip-row">
                    <span class="chip">GitHub, ZIP, or image intake</span>
                    <span class="chip">AI-assisted Dockerfile generation</span>
                    <span class="chip">Guided local deployment preview</span>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

        feature_cols = st.columns(3, gap="medium")
        with feature_cols[0]:
            render_metric_card("Flexible inputs", "Switch between repository links, packaged source archives, and screenshots without changing tools.")
        with feature_cols[1]:
            render_metric_card("Sharper previews", "Review the generated Dockerfile in a cleaner layout before you download or deploy.")
        with feature_cols[2]:
            render_metric_card("Confident handoff", "Keep stack choices and AI state visible so the session feels intentional from the first click.")

    with right_col:
        render_panel_heading(
            "Secure access",
            "Sign in to the workspace",
            "Use the demo credentials to open the assistant and explore the refreshed deployment flow.",
        )
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="1234")
            submitted = st.form_submit_button("Enter workspace", use_container_width=True)

        st.markdown(
            """
            <div class="login-note">
                <strong>Demo access</strong>
                <p>Username: admin and password: 1234.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if submitted:
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.success("Login successful. Opening the deployment workspace.")
                st.rerun()
            else:
                st.error("Invalid credentials. Use the demo access shown below the form.")


if not st.session_state.logged_in:
    login()
    st.stop()

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="small-kicker">Smart Deployment</div>
            <h2>Workspace controls</h2>
            <p>Shape the project profile before generating the Dockerfile preview.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    project_type = st.selectbox("Project type", ["Python", "Node", "Java"])
    use_ai = st.toggle("Use AI assistance", value=True)
    st.markdown(
        """
        <div class="sidebar-card">
            <strong>Session tip</strong>
            <p>Keep AI enabled for the fastest route to a usable Dockerfile draft. Toggle it off only if you want to test the fallback behavior.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.docker_result = None
        st.session_state.deploy_url = None
        st.session_state.last_status = None
        st.rerun()

st.markdown(
    """
    <section class="hero-banner">
        <span class="eyebrow">Smart Deployment Assistant</span>
        <h1>From project context to a launch-ready Dockerfile in one focused workspace.</h1>
        <p>Select how you want to share source context, generate a stack-aware Dockerfile, and move into download or deploy actions without losing sight of the session setup.</p>
        <div class="chip-row">
            <span class="chip">Project profile: Python, Node, or Java</span>
            <span class="chip">Responsive command center layout</span>
            <span class="chip">Preview deploy after generation</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(3, gap="medium")
with metric_cols[0]:
    render_metric_card("Input modes", "Choose between a repository URL, ZIP upload, or image upload depending on how the project arrives.")
with metric_cols[1]:
    render_metric_card("Generation path", "The assistant translates the selected stack into a Dockerfile draft with lightweight validation.")
with metric_cols[2]:
    render_metric_card("Deployment handoff", "Download the result or trigger a preview deployment once the output looks right.")

input_col, output_col = st.columns([0.92, 1.08], gap="large")

with input_col:
    render_panel_heading(
        "Input setup",
        "Tell the assistant what to work with",
        "Pick the project source and provide the minimum context needed for Dockerfile generation.",
    )

    option = st.radio(
        "Select input method",
        ["GitHub Repo", "Upload ZIP", "Upload Image"],
        horizontal=True,
    )

    repo_url = None
    zip_file = None
    uploaded_file = None

    if option == "GitHub Repo":
        repo_url = st.text_input("GitHub URL", placeholder="https://github.com/your-org/your-repo")
        st.markdown('<p class="subtle-note">Paste a repository link so the assistant can treat the source as a remote project.</p>', unsafe_allow_html=True)
    elif option == "Upload ZIP":
        zip_file = st.file_uploader("Upload a ZIP archive", type=["zip"])
        st.markdown('<p class="subtle-note">Upload a packaged codebase when the project is not available through a public repository.</p>', unsafe_allow_html=True)
    else:
        uploaded_file = st.file_uploader("Upload a project image", type=["png", "jpg", "jpeg"])
        st.markdown('<p class="subtle-note">Share an image when the assistant should infer the project type from a screenshot or diagram.</p>', unsafe_allow_html=True)
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded reference", use_container_width=True)

    st.markdown(
        f"""
        <div class="panel-card">
            <strong>Detected profile</strong>
            <p>The workspace is currently configured for <strong>{project_type}</strong> projects with <strong>{option}</strong> as the active intake path.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Generate Dockerfile", use_container_width=True):
        st.session_state.deploy_url = None
        st.session_state.last_status = None

        if option == "GitHub Repo" and not repo_url:
            st.session_state.docker_result = None
            st.session_state.last_status = ("error", "Enter a GitHub URL before generating the Dockerfile.")
        elif option == "Upload ZIP" and not zip_file:
            st.session_state.docker_result = None
            st.session_state.last_status = ("error", "Upload a ZIP archive before generating the Dockerfile.")
        elif option == "Upload Image" and not uploaded_file:
            st.session_state.docker_result = None
            st.session_state.last_status = ("error", "Upload an image before generating the Dockerfile.")
        else:
            with st.spinner("Preparing your Dockerfile preview..."):
                time.sleep(1.2)
                if option == "GitHub Repo":
                    input_data = f"{project_type} project from GitHub repo: {repo_url}"
                elif option == "Upload ZIP":
                    input_data = f"{project_type} project from zip"
                else:
                    input_data = f"{project_type} project from image"

                result = generate_dockerfile(input_data, use_ai)

            if not use_ai:
                st.session_state.docker_result = None
                st.session_state.last_status = ("error", "AI assistance is disabled, so generation could not proceed.")
            elif result is None:
                st.session_state.docker_result = None
                st.session_state.last_status = ("error", "The assistant could not build a Dockerfile for this input.")
            else:
                st.session_state.docker_result = result
                st.session_state.last_status = ("success", "Dockerfile generated successfully. Review the output before download or deploy.")

with output_col:
    render_panel_heading(
        "Output",
        "Review the generated Dockerfile",
        "This panel keeps the result, download action, and preview deployment together so the next step stays obvious.",
    )

    if st.session_state.last_status:
        status_type, message = st.session_state.last_status
        getattr(st, status_type)(message)

    if st.session_state.docker_result:
        st.code(st.session_state.docker_result, language="dockerfile")
        action_cols = st.columns(2, gap="medium")
        with action_cols[0]:
            st.download_button(
                "Download Dockerfile",
                st.session_state.docker_result,
                file_name="Dockerfile",
                use_container_width=True,
            )
        with action_cols[1]:
            if st.button("Deploy preview", use_container_width=True):
                with st.spinner("Launching deployment preview..."):
                    time.sleep(1.8)
                st.session_state.deploy_url = "https://your-app.streamlit.app"
                st.success("Preview deployment is ready.")

        if st.session_state.deploy_url:
            st.markdown(
                f"""
                <div class="panel-card">
                    <strong>Preview environment</strong>
                    <p>Your sample deployment endpoint is <strong>{st.session_state.deploy_url}</strong>.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="empty-state">
                <strong>Nothing generated yet</strong>
                <p>Once you provide the project context and run generation, the Dockerfile preview will appear here together with download and deploy actions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
