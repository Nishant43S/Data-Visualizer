import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_option_menu import option_menu
from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
import io

#### importing libraries

st.set_page_config(   ### setting page layout
    page_title="Data Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state='collapsed'   
)


### functions

@st.cache_data
def load_data(file):
    return pd.read_csv(file)


@st.cache_data
def File_name(file)->str:
    if file is not None:
        return file.name[:-4]


def insert_css(file):
    with open(file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

##### adding side bar
app_sidebar = st.sidebar

with app_sidebar:
    st.subheader("Data Visualizer📊")
    st.text("")
    st.text("")

    Main_menu = option_menu(  #### main menu
        menu_title="",
        options=["Data Visualizer","App Info"],
        icons=["file-bar-graph","person-circle"]
    )

    uploaded_file = st.file_uploader(   #### file uploader
        label="Upload CSV file", 
        type=["csv"]
    )
    


if Main_menu == "Data Visualizer":

    if uploaded_file is not None:
            
        def Data_Visualizer(file):  #### data Visualizer
            try:
                global df
                df = load_data(file)
                pyg_app = StreamlitRenderer(df,appearance="light")
                pyg_app.explorer()
               
            except Exception as err:
                st.warning(f"Error...\n\n{err}")

            st.text("")
            st.text("")
            st.text("")
            st.text("")
            st.markdown("<h6 style='text-align: center;'>Created by Nishant Maity</h6>",unsafe_allow_html=True)
            
        def data_statistics():
            data_head, data_tail = st.columns(2,gap="medium")  #### head and tail of dataframe
            with data_head:
                st.subheader("Head")
                st.dataframe(df.head(),use_container_width=True,key=1)
            with data_tail:
                st.subheader("Tail")
                st.dataframe(df.tail(),use_container_width=True,key=2)

            ##### descriptive statistics 

            descriptive_stat , stat_selectbox = st.columns([3,3],gap="small") 

            with descriptive_stat:
                st.subheader("Descriptive Statistics ")
            with stat_selectbox:
               
                include_box = st.selectbox(
                        label="select type",
                        options=[None,"all",object,np.number],
                        label_visibility="hidden",key=1
                )
                
            try:
                st.dataframe(
                    df.describe(include=include_box),use_container_width=True
                )  ### data describe
            except :
                st.warning("No objects to concatenate")

            
            data_info , unique_value , null_value = st.columns([6,5,4],gap="small")

            with data_info:  ### data info
                with st.container(border=True,height=400):
                    try:
                        st.subheader("Data Info")
                        buffer = io.StringIO()
                        df.info(buf=buffer)
                        info_str = buffer.getvalue()
                        # Remove the unwanted line
                        filtered_info = "\n".join([line for line in info_str.split("\n") if "<class" not in line])
                        st.text(filtered_info)
                    except :
                        st.warning("Something went wrong")
            
            with unique_value:  ##3 unique values
                with st.container(border=True,height=400):
                    st.subheader("Unique Values")
                    st.text(df.nunique())

            with null_value:  ### null values
                with st.container(border=True,height=400):
                    st.subheader("Null Values")
                    st.text(df.isnull().sum())

            st.text("")
            st.text("")
            st.text("")
            st.text("")
            st.markdown("<h6 style='text-align: center;'>Created by Nishant Maity</h6>",unsafe_allow_html=True)


        def Data_plots():  ### plots
            st.subheader("Data Plots")   

            df_columns =  [None]+list(df.columns)      

            select_section , plot_section  = st.columns([4,7],gap="large")     

            with select_section:
                st.write("use x axis for countplot, boxplot, histogram ")
                try:
                    ### setting x and y axis of the plots
                    X_axis = st.selectbox(label="X axis",options=df_columns,key="xaxis")            
                    Y_axis = st.selectbox(label="Y axis",options=df_columns,key="yaxis") 

                    plot_type = [
                        None,"Line Plot","Bar Chart",
                        "Box Plot","Histogram","Scatter Plot",
                        "Count Plot"
                    ]           

                    Select_plot = st.selectbox(label="Plot Type",options=plot_type,key="Plot type")


                    #### generate plot function
                    @st.cache_data
                    def generated_plot(x_axis,y_axis,generated_plot_type):
                        try:
                            fig , ax = plt.subplots(figsize=(4,2))
                            
                            ### plots
                            if generated_plot_type == "Line Plot":
                                sbn.lineplot(x=df[x_axis],y=df[y_axis],ax=ax)

                            elif generated_plot_type == "Bar Chart":
                                sbn.barplot(x=df[x_axis],y=df[y_axis],ax=ax)

                            elif generated_plot_type == "Box Plot":
                                sbn.boxplot(x=df[x_axis],ax=ax)

                            elif generated_plot_type == "Scatter Plot":
                                sbn.scatterplot(x=df[x_axis],y=df[y_axis],ax=ax)

                            elif generated_plot_type == "Histogram":
                                sbn.histplot(x=df[x_axis],ax=ax)

                            elif generated_plot_type == "Count Plot":
                                sbn.countplot(x=df[x_axis],ax=ax)

                            ax.tick_params(axis="x",labelsize=6)
                            ax.tick_params(axis="y",labelsize=6)

                            st.pyplot(fig=fig)
                        except Exception as err:
                            st.warning("Error...\n\n",err)

                    if st.button(label="Generate Plot",key="generate plot"):
                        with plot_section:
                            with st.spinner(f"Generating {Select_plot}..."):

                                if __name__=="__main__":
                                    try:
                                        generated_plot(X_axis,Y_axis,Select_plot)
                                    except Exception as err:
                                        st.warning("Error...\n\n",err)

                except Exception as err:
                    st.warning("Unable to plot",err)

          
        colored_header(
            label=f"Visualization of {File_name(uploaded_file)}",
            description="Visualization of your dataset",
            color_name="violet-70"
        )

        with st.spinner("Generating data..."):
            data_visualization , data_stat ,data_plots = st.tabs(["Data Visualization","Data Statistics","Data Plots"])

            with data_visualization:   
                if __name__=="__main__":  ### data visualization
                    Data_Visualizer(uploaded_file)

            with data_stat:
                if __name__=="__main__":  ### data statstics
                    data_statistics()

            with data_plots: ### data plots
                if __name__=="__main__":
                    Data_plots()
                
            
    else:
        st.info("Upload csv file")


if Main_menu == "App Info":
    def insert_html(file):
        with open(file) as f:
            st.markdown(f.read(),unsafe_allow_html=True)
    
    if __name__=="__main__":
        insert_html("about_app.html")
       
if __name__=="__main__":
    insert_css("style.css")