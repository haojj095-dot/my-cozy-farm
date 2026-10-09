import datetime
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="My Cozy Project Farm", page_icon="🌾", layout="centered"
)

# Custom Theme Styling (Cozy Farm Aesthetic)
st.markdown(
    """
    <style>
    .main {
        background-color: #F9F6F0;
    }
    .stButton>button {
        background-color: #557A46;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #3C5A32;
        color: white;
    }
    .farm-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 6px solid #557A46;
    }
    .farm-card-hungry {
        background-color: #FFF9F0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 6px solid #D97706;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State Data
if "projects" not in st.session_state:
    st.session_state.projects = [
        {
            "id": 1,
            "title": "Q4 Compliance Audit & Workflow Redesign",
            "category": "Work",
            "animal_type": "Cow 🐮",
            "description": "Streamlining corporate secretarial files and review processes.",
            "subquests": [
                {"task": "Map out current workflow bottlenecks", "done": True},
                {
                    "task": "Draft updated checklist templates",
                    "done": False,
                },
                {"task": "Test with pilot client portfolio", "done": False},
            ],
            "last_touched": str(datetime.date.today()),
            "status": "Thriving",
        },
        {
            "id": 2,
            "title": "Compound Leg Strength & Squat Mobility",
            "category": "Gym",
            "animal_type": "Horse 🐴",
            "description": "Progressive overload on Zercher squats and sumo deadlifts.",
            "subquests": [
                {"task": "Establish baseline working weights", "done": True},
                {"task": "Integrate weekly mobility stretching", "done": True},
                {
                    "task": "Hit new personal record milestone",
                    "done": False,
                },
            ],
            "last_touched": str(
                datetime.date.today() - datetime.timedelta(days=6)
            ),
            "status": "Hungry",
        },
    ]

if "chores" not in st.session_state:
    st.session_state.chores = {
        "Sweep the Barn (Daily Journal / Review)": False,
        "Water the Garden (Hydration & Stretching)": True,
        "Mend the Fences (Inbox Zero & Tidy Desk)": False,
    }

# App Header
st.title("🌾 My Cozy Farmstead")
st.write(
    "Welcome back, Farmer! Tend to your daily chores and grow your livestock by making small bites of progress."
)
st.divider()

# Sidebar Navigation
tab = st.radio(
    "Farm Sections",
    ["🏡 Pasture (Projects)", "🧹 Barn Chores (Habits)", "➕ Plant New Project"],
    horizontal=True,
)

# ---------------------------------------------------------
# TAB 1: PASTURE (PROJECTS & LIVESTOCK)
# ---------------------------------------------------------
if tab == "🏡 Pasture (Projects)":
    st.subheader("Your Livestock & Projects")

    # Filter by category
    category_filter = st.selectbox(
        "Filter Pasture Zone:", ["All", "Work", "Gym", "Personal"]
    )

    for p in st.session_state.projects:
        if category_filter != "All" and p["category"] != category_filter:
            continue

        # Calculate progress from subquests
        total_quests = len(p["subquests"])
        completed_quests = sum(1 for sq in p["subquests"] if sq["done"])
        progress_pct = (
            int((completed_quests / total_quests) * 100)
            if total_quests > 0
            else 0
        )

        # Check staleness (> 4 days = hungry/sluggish animal)
        last_date = datetime.date.fromisoformat(p["last_touched"])
        days_inactive = (datetime.date.today() - last_date).days

        is_hungry = days_inactive > 4
        card_class = "farm-card-hungry" if is_hungry else "farm-card"

        with st.container():
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f"### {p['animal_type']} {p['title']} [{p['category']}]"
                )
                st.write(f"*{p['description']}*")
            with col2:
                if is_hungry:
                    st.warning(
                        f"⚠️ Sluggish! Inactive for {days_inactive} days."
                    )
                else:
                    st.success("✨ Thriving & Growing!")

            # Health Bar / Growth Meter
            st.write(
                f"**Growth Progress ({progress_pct}% - {completed_quests}/{total_quests} Sub-Quests Done)**"
            )
            st.progress(progress_pct / 100)

            # Sub-Quests Checkboxes
            st.text("Micro-Bites (Check off to grow your animal):")
            for idx, sq in enumerate(p["subquests"]):
                checkbox_key = f"proj_{p['id']}_sq_{idx}"
                is_checked = st.checkbox(
                    sq["task"], value=sq["done"], key=checkbox_key
                )
                if is_checked != sq["done"]:
                    p["subquests"][idx]["done"] = is_checked
                    p["last_touched"] = str(datetime.date.today())
                    st.rerun()

            # Quick Log Interaction to feed the animal
            with st.expander("🍎 Feed Animal / Log Quick Progress Note"):
                quick_note = st.text_input(
                    "What did you do today?", key=f"note_{p['id']}"
                )
                if st.button("Feed & Update Timestamp", key=f"btn_{p['id']}"):
                    if quick_note:
                        p["last_touched"] = str(datetime.date.today())
                        st.success(
                            f"Fed {p['animal_type']}! Progress note saved. Energy restored!"
                        )
                        st.rerun()
                    else:
                        st.warning("Please write a short note first.")

            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: BARN CHORES (HABITS)
# ---------------------------------------------------------
elif tab == "🧹 Barn Chores (Habits)":
    st.subheader("Daily Farm Chores")
    st.write(
        "Clear these out daily to keep the farm grounds clean and running smoothly."
    )

    for chore, status in st.session_state.chores.items():
        new_status = st.checkbox(chore, value=status)
        if new_status != status:
            st.session_state.chores[chore] = new_status
            st.rerun()

    all_done = all(st.session_state.chores.values())
    if all_done:
        st.balloons()
        st.success(
            "🌟 All chores completed! The farm is pristine and shining today!"
        )

# ---------------------------------------------------------
# TAB 3: PLANT NEW PROJECT
# ---------------------------------------------------------
elif tab == "➕ Plant New Project":
    st.subheader("Adopt a New Livestock / Project")

    with st.form("new_project_form"):
        new_title = st.text_input("Project Name")
        new_desc = st.text_input("Short Description / Goal")
        new_cat = st.selectbox("Category", ["Work", "Gym", "Personal"])
        new_animal = st.selectbox(
            "Choose Your Livestock", ["Cow 🐮", "Horse 🐴", "Sheep 🐑", "Pig 🐷"]
        )

        st.text("Initial Micro-Bites (Break it down into small pieces):")
        bites = [
            st.text_input("Micro-Bite 1", value="Initial setup or research"),
            st.text_input("Micro-Bite 2", value="Execute core phase"),
            st.text_input("Micro-Bite 3", value="Review and finalize"),
        ]

        submitted = st.form_submit_button("Adopt & Plant to Pasture")
        if submitted and new_title:
            valid_bites = [
                {"task": b, "done": False} for b in bites if b.strip() != ""
            ]
            new_id = len(st.session_state.projects) + 1
            st.session_state.projects.append(
                {
                    "id": new_id,
                    "title": new_title,
                    "category": new_cat,
                    "animal_type": new_animal,
                    "description": new_desc,
                    "subquests": valid_bites,
                    "last_touched": str(datetime.date.today()),
                    "status": "Thriving",
                }
            )
            st.success(
                f"🎉 Successfully welcomed your new {new_animal} to the pasture!"
            )
