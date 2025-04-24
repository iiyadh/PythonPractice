import streamlit as st
import requests

st.write("## User GitHub Profile")
user_input = st.text_input("Enter GitHub username:")


url = f"https://api.github.com/users/{user_input}"

if st.button("Get Profile", key="get_profile"):
    if user_input:
        response = requests.get(url)
        if response.status_code == 200:
            profile_data = response.json()
            st.write("### Profile Information")
            st.write(f"**Name:** {profile_data.get('login', 'N/A')}")
            st.image(profile_data.get('avatar_url', 'N/A'), width=100)
            st.write(f"**Bio:** {profile_data.get('bio', 'N/A')}")
            st.write(f"**Public Repos:** {profile_data.get('public_repos', 'N/A')}")
            st.write(f"**Followers:** {profile_data.get('followers', 'N/A')}")
            st.write(f"**Following:** {profile_data.get('following', 'N/A')}")
            st.write(f"[View Profile]({profile_data.get('html_url', '#')})")
        else:
            st.error("User not found or an error occurred.")
    else:
        st.warning("Please enter a GitHub username.")