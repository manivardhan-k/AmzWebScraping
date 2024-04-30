import numpy as np
import pandas as pd
import AmzExtract as a
import webbrowser as wb
import streamlit as st
import matplotlib.pylab as plt
import os
from pathlib import Path
import math

st.set_page_config(page_title="VegaNex", page_icon=":anchor:", layout="wide", initial_sidebar_state="expanded")

st.header('Welcome to **:green[VegaNex]**!', divider='red')

entry = st.text_input('**What would you like to browse today?**', placeholder="Enter text")

if entry:
    try: # check for error in think chunk
        desktop_path = Path(os.path.expanduser("~/Desktop"))
        my_df = pd.read_csv(f"{desktop_path}/{entry}.csv")
        del my_df['Unnamed: 0']
    except:
        my_df = a.extract(entry)

    # st.write(my_df)

    # -- SIDEBAR --
    with st.sidebar:
        st.header("Menu Bar")

        sort = st.radio(
            "**Choose a sort by option:**",
            ("Relevance", "Price (Low-High)", "Price (High-Low)", "Discount")
        )

        max = int(round(max(my_df['Discounted_Price'])))+1
        price_range = []
        for i in range(0, max+1):
            price_range.append(f'${str(i)}')

        start_price, end_price = st.select_slider(
            "**Choose the price range**",
            options=price_range,
            value=('$0', f'${max}'))
    # -- SIDEBAR --

    # -- FILTER --
    my_df = my_df.query(f'{start_price[1:]} <= Discounted_Price <= {end_price[1:]}')
    # -- FILTER --

    # -- SORT --
    if sort == "Relevance":
        my_df = my_df.sort_values(by=['Formula'])
    elif sort == "Price (Low-High)":
        my_df = my_df.sort_values(by=['Discounted_Price'])
    elif sort == "Price (High-Low)":
        my_df = my_df.sort_values(by=['Discounted_Price'], ascending=False)
    elif sort == "Discount":
        my_df = my_df.sort_values(by=['Discount'], ascending=False)
    # -- SORT --

    st.divider()

    # -- BOXPLOT --
    my_df_image = my_df.Discounted_Price.to_list()
    my_df_image = np.array(my_df_image)
    fig = plt.figure(figsize =(10, 2))
    bp = plt.boxplot(my_df_image, vert=0)
    plt.grid(axis='x')
    plt.title("Box Plot of Prices ($)")
    plt.savefig(f'{entry}.png')
    st.image(f'{entry}.png')
    # -- BOXPLOT --

    st.divider()

    st.subheader(f'Here are the results for {entry}:')

    def page():
        if "amazon_list" not in st.session_state:
            st.session_state["amazon_list"]=0
        st.session_state["amazon_list"] = []

        # -- PAGES & DFS --
        total_pages = math.ceil(len(my_df)/20)

        pages=[]
        for i in range(total_pages):
            pages.append(f"Page {i+1}")

        dfs = {}
        for i in range(total_pages):
            dfs[f"df{i+1}"] = my_df[0+(20*i):20+(20*i)]

        dfs_list = list(dfs.values())

        tabs = st.tabs(pages)

        count = 0
        for i in range(total_pages):
            with tabs[i]:

        # -- PAGES & DFS --

                for j in range(len(dfs_list[i])):
                    with st.container(border=True):
                        col1, col2 = st.columns([0.2, 0.8])
                        with col1:
                            # -- IMAGE --
                            with st.container(border=True):
                                st.image(dfs_list[i].iloc[j, 2], use_column_width='auto')
                            # -- IMAGE --
                        with col2:
                            # -- CONTENT --
                            with st.container(border=True):
                                st.write(f"**{dfs_list[i].iloc[j, 0]}**")
                                if 1 <= dfs_list[i].iloc[j, 3] < 2:
                                    with st.popover("**Rating:** "+" :star:"):
                                        st.markdown(f"**Rating:** {dfs_list[i].iloc[j, 3]} " + " :star:")
                                        st.markdown(f"**Total Ratings:** {dfs_list[i].iloc[j, 4]}")
                                if 2 <= dfs_list[i].iloc[j, 3] < 3:
                                    with st.popover("**Rating:** "+" :star:"*2):
                                        st.markdown(f"**Rating:** {dfs_list[i].iloc[j, 3]} " + " :star:"*2)
                                        st.markdown(f"**Total Ratings:** {dfs_list[i].iloc[j, 4]}")
                                if 3 <= dfs_list[i].iloc[j, 3] < 4:
                                    with st.popover("**Rating:** "+" :star:"*3):
                                        st.markdown(f"**Rating:** {dfs_list[i].iloc[j, 3]} " + " :star:"*3)
                                        st.markdown(f"**Total Ratings:** {dfs_list[i].iloc[j, 4]}")
                                if 4 <= dfs_list[i].iloc[j, 3] < 5:
                                    with st.popover("**Rating:** "+" :star:"*4):
                                        st.markdown(f"**Rating:** {dfs_list[i].iloc[j, 3]} " + " :star:"*4)
                                        st.markdown(f"**Total Ratings:** {dfs_list[i].iloc[j, 4]}")
                                if dfs_list[i].iloc[j, 3] == 5:
                                    with st.popover("**Rating:** "+" :star:"*5):
                                        st.markdown(f"**Rating:** {dfs_list[i].iloc[j, 3]} " + " :star:"*5)
                                        st.markdown(f"**Total Ratings:** {dfs_list[i].iloc[j, 4]}")
                                if dfs_list[i].iloc[j, 1] != 0:
                                    st.write(f"**Recent Sales:** {int(dfs_list[i].iloc[j, 1])}")
                                if dfs_list[i].iloc[j, 7] == 0:
                                    st.markdown(f"**Price: :green[${dfs_list[i].iloc[j, 5]}]**")
                                else:
                                    st.markdown(f"**Price: :red[${dfs_list[i].iloc[j, 6]}] :point_right: :green[${dfs_list[i].iloc[j, 5]}]  :green[(Save ${round(dfs_list[i].iloc[j, 7],2)})]**")

                                st.write(f":point_right: **[Amazon Link]({dfs_list[i].iloc[j, 9]})** :point_left:")
                            # -- CONTENT --

                                # -- LIST FEATURE -- 
                                check = st.checkbox("Add to amazon list", key = count)
                                count +=1
                                if check:
                                    st.session_state["amazon_list"].append(dfs_list[i].iloc[j, 9])
                                #  -- LIST FEATURE -- 

        # -- OPEN AMAZON --
        if st.session_state["amazon_list"]:
            with st.sidebar:
                if st.button('Open my list on Amazon'):
                    for i in st.session_state["amazon_list"]:
                        wb.open_new_tab(i)
        # -- OPEN AMAZON --

    page()

# streamlit run Webpage.py
