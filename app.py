import streamlit as st
import utils

# Custom CSS for DeepSeek-like UI
def load_css():
    st.markdown(
        """
        <style>
        /* Main background color */
        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }

        /* Table styling */
        .stDataFrame {
            background-color: #1F2A3C;
            color: #FFFFFF;
            font-size: 18px;  /* Increase font size */
            width: 100%;      /* Make the table wider */
        }

        /* Table header styling */
        .stDataFrame th {
            font-size: 20px;  /* Increase header font size */
            padding: 12px;    /* Add padding to header cells */
        }

        /* Table cell styling */
        .stDataFrame td {
            font-size: 18px;  /* Increase cell font size */
            padding: 10px;    /* Add padding to cells */
        }

        /* Table hover effect */
        .stDataFrame tr:hover {
            background-color: #2C3A4D;  /* Change hover color */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Page configuration
st.set_page_config(page_title="Student Result Analysis", layout="wide")

# Load custom CSS
load_css()

# Admin login
def admin_login():
    st.sidebar.title("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "Admin@123":
            st.session_state.logged_in = True
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid credentials")

# Dashboard
def dashboard():
    st.title("🎓 Student Result Analysis Dashboard")

    # Fetch data from the database
    query = "SELECT * FROM students"
    df = utils.fetch_data(query)

    # Display options in the sidebar
    st.sidebar.title("Options")
    option = st.sidebar.selectbox(
        "Select an option",
        [
            "Highest Mark",
            "Subjectwise Analysis",
            "Fail or Pass",
            "Top 5",
            "List of Failures",
            "Subjectwise Pass or Fail",
            "Compare Marks and Attendance",
            "Report Generation"
        ]
    )

    if option == "Highest Mark":
        st.subheader("🏆 Highest Mark")
        highest_mark = df[df['marks'] == df['marks'].max()]
        st.write(highest_mark)

    elif option == "Subjectwise Analysis":
        st.subheader("📊 Subjectwise Analysis")
        subject = st.selectbox("Select Subject", df['subject'].unique())
        subject_data = df[df['subject'] == subject]
        st.write(subject_data)

    elif option == "Fail or Pass":
        st.subheader("✅ Fail or Pass")
        df['status'] = df['marks'].apply(utils.calculate_pass_fail)
        st.write(df[['name', 'subject', 'marks', 'status']])

    elif option == "Top 5":
        st.subheader("🥇 Top 5 Students")
        top_5 = utils.get_top_students(df)
        st.write(top_5)

    elif option == "List of Failures":
        st.subheader("❌ List of Failures")
        failures = utils.get_failures(df)
        st.write(failures)

    elif option == "Subjectwise Pass or Fail":
        st.subheader("📚 Subjectwise Pass or Fail")
        subject = st.selectbox("Select Subject", df['subject'].unique())
        subject_data = df[df['subject'] == subject]
        subject_data['status'] = subject_data['marks'].apply(utils.calculate_pass_fail)
        st.write(subject_data)

    elif option == "Compare Marks and Attendance":
        st.subheader("📈 Compare Marks and Attendance")
        st.scatter_chart(df, x='attendance', y='marks')

    elif option == "Report Generation":
        st.subheader("📄 Report Generation")
        st.write("Generating report...")
        report = utils.generate_report(df)
        st.write(report)
        st.download_button(
            label="Download Report",
            data=report.to_csv(index=False).encode('utf-8'),
            file_name='student_report.csv',
            mime='text/csv'
        )

# Main app logic
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        admin_login()
    else:
        dashboard()

if __name__ == "__main__":
    main()