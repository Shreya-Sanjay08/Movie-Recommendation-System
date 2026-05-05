

import streamlit as st
from backend.recommender import recommend_movies, movies_data, get_genre_distribution
from backend.tmdb_utils import search_movie, get_poster_url, get_overview, get_top_popular_movies
from backend.firebase_utils import sign_in, sign_up, update_list, get_user_lists
import plotly.express as px

# Setup
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Session state init
if 'user' not in st.session_state:
    st.session_state.user = None

# Main Application
def app_ui():
    st.title("🎥 Movie Recommendation System")

    # Sidebar with navigation
    st.sidebar.title("Explore More")
    section = st.sidebar.radio("Go to", ["Get Recommendations", "Genre Distribution", "Top 10 Popular Movies", "My Lists"])
    # st.sidebar.markdown(f"👤 {st.session_state.user['email']}")
    

    if section == "Get Recommendations":
        movie_input = st.text_input("Enter a movie you like")
        if st.button("Get Recommendations"):
            if movie_input:
                results = recommend_movies(movie_input)
                if results:
                    st.subheader("🎯 Recommended Movies")
                    for title in results:
                        movie_data = search_movie(title)
                        if movie_data:
                            poster = get_poster_url(movie_data)
                            overview = get_overview(movie_data)

                            col1, col2 = st.columns([1, 4])
                            with col1:
                                if poster:
                                    st.image(poster, width=120)
                            with col2:
                                st.markdown(f"**{title}**")
                                st.write(overview)
                                st.write("Add to:")
                                c1, c2, c3 = st.columns(3)
                                if c1.button(f"❤️ Favorite {title}", key=f"fav_{title}"):
                                    update_list(st.session_state.user['email'], "favorites", title)
                                    st.success(f"{title} added to Favorites")
                                if c2.button(f"✅ Watched {title}", key=f"watched_{title}"):
                                    update_list(st.session_state.user['email'], "watched", title)
                                    st.success(f"{title} added to Watched")
                                if c3.button(f"📌 Want {title}", key=f"want_{title}"):
                                    update_list(st.session_state.user['email'], "want_to_watch", title)
                                    st.success(f"{title} added to Want to Watch")
                            st.markdown("---")
                else:
                    st.warning("Movie not found. Try a different title.")

    elif section == "Genre Distribution":
        st.subheader("🎭 Top Genres in the Dataset")
        genre_counts = get_genre_distribution(movies_data)
        fig = px.bar(genre_counts, x=genre_counts.index, y=genre_counts.values, labels={'x': 'Genre', 'y': 'Count'})
        st.plotly_chart(fig, use_container_width=True)

    elif section == "Top 10 Popular Movies":
        st.subheader("🔥 Top 10 Popular Movies (Live from TMDB)")
        popular = get_top_popular_movies()
        for movie in popular:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(get_poster_url(movie), width=120)
            with col2:
                st.markdown(f"**{movie['title']}**")
                st.write(get_overview(movie))
            st.markdown("---")

    elif section == "My Lists":
        st.subheader("🗂️ Your Saved Lists")
        lists = get_user_lists(st.session_state.user['email'])
        for list_type in ["favorites", "watched", "want_to_watch"]:
            st.markdown(f"### {list_type.capitalize()}")
            if list_type in lists and lists[list_type]:
                for title in lists[list_type]:
                    st.markdown(f"- 🎬 {title}")
            else:
                st.markdown("No movies added yet.")

# Entry Point
# if st.session_state.user:
app_ui()


