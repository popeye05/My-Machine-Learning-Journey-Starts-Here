import streamlit as st
import pickle

games_df = pickle.load(open('games.pkl','rb'))
names_only = games_df['name'].values
similarity = pickle.load(open('similarity.pkl','rb'))
#Now the 'recommend' funtion
def recommend(game):

    game_index = games_df[games_df['name'] == game].index[0]
    distances = similarity[game_index]
    top_matches = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    y = []
    for i in top_matches:
        y.append(games_df.iloc[i[0]]['name'])
    return y
st.title("Similar Games 4 U: ")
game = st.selectbox(
    "If You Like The Below Game, You Might like these Other Games. Developed by Popeye @ 2025",
    names_only,
)
if st.button('Select'):
    st.write(f"**{game}** is a good game. But you might wanna try these instead :)")
    output = recommend(game)
    for i in output:
        st.write(i)
