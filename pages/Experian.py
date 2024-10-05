import streamlit as st
import pandas as pd
import plotly.express as px
from lxml import etree
import io

# Load the XML file
def load_xml(file):
    try:
        tree = etree.parse(file)
        root = tree.getroot()
        return root
    except Exception as e:
        st.error(f"Error loading XML file: {e}")
        return None

#Extracting Of Raw And Aggregated data from Xml file
def extract_data_for_account_lxml(element):
    raw_data = []
    aggregated_data = []

    interface_aggregations = element.xpath(".//InterfaceAggregations")

    for interface in interface_aggregations:
        aggregation_locals = interface.xpath(".//AggregationLocal")
        for agg_local in aggregation_locals:
            raw_items = agg_local.xpath("./Raw")
            for raw_item in raw_items:
                name = raw_item.get("Name")
                value = raw_item.get("Value")
                raw_data.append({"Name": name, "Value": value})

            aggregated_items = agg_local.xpath("./Aggregated")
            for agg_item in aggregated_items:
                name = agg_item.get("Name")
                value = agg_item.get("Value")
                description = agg_item.get("Description")

                group_number = None
                
                if "G1" in name:
                    group_number = 1  
                elif "G2" in name:
                    group_number = 2  
                elif "G3" in name:
                    group_number = 3  
                elif "G4" in name:
                    group_number = 4  
                elif "G5" in name:
                    group_number = 5  
                elif "G6" in name:
                    group_number = 6  
                elif "G7" in name:
                    group_number = 7  
                elif "G8" in name:
                    group_number = 8  
                elif "G9" in name:
                    group_number = 9  
                elif "G10" in name:
                    group_number = 10 
                else:
                    group_number = 11
                    
                group_number = min(group_number, 11)
                
#Adding the code in  aggregated_data
                aggregated_data.append({
                    "Name": name,
                    "Value": value,
                    "Description": description,
                })

  # Sorting The aggreagated data in sorting format
    aggregated_data = sorted(aggregated_data, key=lambda x: x["Name"])

    return raw_data, aggregated_data
    
# Code Of the Raw Button    
def raw_page():
    st.title("Raw Data Table")

    file = './1_Account_035_Result.xml'
    root = load_xml(file)

    if root is None:
        st.error("Failed to load XML file.")
        return

    # Extract raw data using the existing function
    raw_data, _ = extract_data_for_account_lxml(root)

    if raw_data:
        # Convert raw data to a DataFrame for display
        raw_df = pd.DataFrame(raw_data)
        st.table(raw_df)  # Display the raw data in a table format
    else:
        st.write("No Raw Data Found.")

# Extract psummary data for analysis
def extract_psummary_data(root):
    psummary_data = []
    
    for psummary in root.xpath(".//PSUMMARY"):
        creditor_name = psummary.findtext("CreditorName", default="N/A")
        first_reported_limit_amt = int(psummary.findtext("FirstReportedLimitAmt", default=0))
        current_limit = int(psummary.findtext("CurrentLimit", default=0))
        account_status = psummary.findtext("AccountStatus", default="N/A")
        credit_card_type = psummary.findtext("CreditCardType", default="N/A")
        
        psummary_data.append({
            'CreditorName': creditor_name,
            'FirstReportedLimitAmt': first_reported_limit_amt,
            'CurrentLimit': current_limit,
            'AccountStatus': account_status,
            'CreditCardType': credit_card_type  
        })
        
    return pd.DataFrame(psummary_data)

# Analyze page display
def analyze_page():
    st.subheader("Analysis Page")
    
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.error("No data available to plot. Please check the XML file.")
        return

    data = st.session_state.data
    graph_type = st.selectbox("Select a graph type to display:", ["Line Graph", "Bar Graph", "Pie Chart"])
    
    chart_placeholder = st.empty()

    with chart_placeholder.container():
        if graph_type == "Line Graph":
            st.subheader("Line Graph of FirstReportedLimitAmt by Creditor Name")
            line_fig = px.line(data, x='CreditorName', y='FirstReportedLimitAmt', title="First Reported Limit Amount by Creditor Name")
            st.plotly_chart(line_fig)

        elif graph_type == "Bar Graph":
            st.subheader("Bar Graph of CurrentLimit by Creditor Name")
            bar_fig = px.bar(data, x='CreditorName', y='CurrentLimit', title="Current Limit by Creditor Name")
            st.plotly_chart(bar_fig)

        elif graph_type == "Pie Chart":
            st.subheader("Pie Chart of Account Status (Open vs Closed)")
            filtered_data = data[data['AccountStatus'].isin(['Open', 'Closed'])]
            if filtered_data.empty:
                st.error("No data available for Open or Closed accounts.")
                return

            pie_data = filtered_data['AccountStatus'].value_counts().reset_index()
            pie_data.columns = ['AccountStatus', 'Count']
            pie_fig = px.pie(pie_data, names='AccountStatus', values='Count', title="Distribution of Account Statuses")
            st.plotly_chart(pie_fig)

#Download the XML File of Request      
def download_xml_button(xml_content, filename):
    xml_bytes = io.BytesIO()
    xml_bytes.write(xml_content.encode('utf-8'))
    xml_bytes.seek(0)
    st.download_button(
        label=f"Download {filename}",
        data=xml_bytes,
        file_name=filename,
        mime="application/xml"
)
# Code Of the Request Button 
def  request_page():
    st.write("request")

# Code Of the Response Button 
def  response_page():
    st.write("response")

# Code Of the Demograph Button 
def  demograph_page():
    st.write("demograph")
    
# Code Of the vericheck Button 
def  vericheck_page():
    st.write("vericheck")

# Code Of the aml Button 
def aml_page():
    st.write("aml")

# Code Of the fraud Button 
def fraud_page():
    st.write("fraud")
    
# Code Of the summary Button 
def  summary_page() :
    st.write("summary") 
    
# Extract Provenir ID and Unique ID from XML file
def extract_ids_from_xml(root):
    header_segment = root.find(".//HeaderSegment")
    if header_segment is not None:
        provenir_id = header_segment.get("ProvenirID", "N/A")
        unique_id = header_segment.get("UniqueID", "N/A")
        return provenir_id, unique_id

    return "N/A", "N/A"

# Main function
def main():
    
 #Styling
    st.markdown(""" 
        <style>
        /* Style for the Provenir ID and Reference# */
        .top-info {
            position: absolute; 
            top: 10px; 
            right: 10px; 
            text-align: right; 
            font-size: 12px;
            font-family: Arial, sans-serif;
            color: black;
        }
       
        /* Align the text beside the logo */
        .header-text {
            display: inline-block;
            vertical-align: middle;
            font-family: Arial, sans-serif;
            font-size: 20px;
            font-weight: bold;
            color: black;
        }
      .st-emotion-cache-1vt4y43 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.1rem;
    /* min-height: 1.5rem; */
    margin: 4px;
    line-height: 1.3;
    color: black;
    width: 110px;
    user-select: none;
    background-color: rgb(240 240 240);
    border: 1.5px solid rgb(0 0 0);
}

    @media (max-width: 1024px) {
        .st-emotion-cache-1vt4y43 {
            width: 100%;  /* Make the buttons take full width on smaller screens */
            margin-bottom: 10px;  /* Add space between buttons */
        }
    }

    @media (max-width: 768px) {
        .st-emotion-cache-1vt4y43 {
            font-size: 12px;  /* Reduce the font size for smaller screens */
            padding: 0.2rem 0.6rem;  /* Reduce padding for better fit */
        }
        .st-emotion-cache-165ax5l {
    width: 90% !important;
    margin-bottom: 1rem;
    color: rgb(49, 51, 63);
    border-collapse: collapse;
    border: 1px solid rgba(49, 51, 63, 0.1);
    margin-left: 50px;
}
    }
      @media (max-width: 620px){
    .st-emotion-cache-165ax5l {
    width: 50% !important;
    margin-bottom: 1rem;
    color: rgb(49, 51, 63);
    border-collapse: collapse;
    border: 1px solid rgba(49, 51, 63, 0.1);
    margin-left: 20px;
}
}
.navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: white; /* Change to match your app's theme */
            z-index: 1000; /* Ensure it stays on top of other elements */
            padding: 10px; /* Optional padding */
            border-bottom: 1px solid rgba(0, 0, 0, 0.1); /* Optional border */
        }
        /* Add spacing below header */
        .header-section {
            padding-bottom: 20px;
        }

        </style>
    """, unsafe_allow_html=True)

    # Load the XML file for Provenir_id and Unique_id
    file = './1_Account_035_Result.xml'
    root = load_xml(file)

    if root is None:
        st.error("Failed to load XML file.")
        return

  
    provenir_id, unique_id = extract_ids_from_xml(root)


    st.markdown(f"""
        <div class='top-info'>
        <b>Provenir ID:</b> {provenir_id}<br>
        <b>Unique ID:</b> {unique_id}
        </div>
    """, unsafe_allow_html=True)

    st.image("logo.png", width=200) #logo Arrangment
    
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    # Navbar Buttons
    navbar = st.container()
    with navbar:
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

        with col1:
            if st.button("Request"):
               st.session_state.page = "Request"        
        with col2:
            if st.button("Response"):
                st.session_state.page = "Response"
        with col3:
            if st.button("Demograph"):
                st.session_state.page = "Demograph"
        with col4:
            if st.button("Analyze"):
                st.session_state.page = "analyze"
        with col5:
            if st.button("VeriCheck"):
                st.session_state.page = "VeriCheck"
        with col6:
            if st.button("AML"):
                st.session_state.page = "AML"
        with col7:
            if st.button("Fraud"):
                st.session_state.page = "Fraud"
        with col8:
            if st.button("Raw"):
                st.session_state.page = "Raw"
        with col9:
            if st.button("Aggregated"):
                st.session_state.page = "Aggregated"
        with col10:
            if st.button("Summary"):
                st.session_state.page = "Summary"

    st.markdown('</div>', unsafe_allow_html=True)
                
#Styling
    st.markdown(
        """
        <style>
         .reportview-container {
                background-color: black;  
                color: white;  
                height: 5px;
                width: 100%;
                margin-bottom: 30px;
            }
            .logo-container {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .dataframe {
                margin-right: 500px;
                margin-left:500px;
            }
       
        .st-emotion-cache-13ln4jf {
            max-width: 100% !important;  
            width: 100% !important;      
            padding: 4rem 4rem 10rem !important;
        }
        .css-1lcbmhc {
            padding-left: 0 !important;  
            padding-right: 0 !important; 
        }
        .st-emotion-cache-165ax5l {
           width: 70% !important;
           margin-bottom: 1rem;
            color: rgb(49, 51, 63);
            border-collapse: collapse;
            border: 1px solid rgba(49, 51, 63, 0.1);
            margin-left: 180px; !important;
        }
       .st-emotion-cache-a51556 {
           border-bottom: 1px solid rgba(49, 51, 63, 0.1);
           border-right: 1px solid rgba(49, 51, 63, 0.1);
           vertical-align: middle;
           padding: 0.25rem 0.375rem;
           font-weight: 400;
           color: rgba(49, 51, 63, 0.6);
           display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

#Arrangment of the information on the page
    st.markdown(
        """
        <div class="reportview-container">
           <div class="logo-container">
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if 'page' not in st.session_state:
        st.session_state.page = "search"
    if 'account_number' not in st.session_state:
        st.session_state.account_number = ""

    file = './1_Account_035_Result.xml'
    root = load_xml(file)

    if root is not None and 'data' not in st.session_state:
        st.session_state.data = extract_psummary_data(root)

    if st.session_state.page == "analyze":
        analyze_page()
    elif st.session_state.page == "Raw":
       raw_page()
    elif st.session_state.page == "Response":
       response_page()
    elif st.session_state.page == "Raw":
       raw_page()
    elif st.session_state.page == "Request":
       request_page()
    elif st.session_state.page == "Demograph":
        demograph_page()
    elif st.session_state.page == "VeriCheck":
        vericheck_page()
    elif st.session_state.page == "AML":
        aml_page()
    elif st.session_state.page == "Fraud":
        fraud_page()
    elif st.session_state.page == "Summary":
       summary_page()    
    else:
        st.title("Aggregated Data")
  # Extract raw data using the existing function
        raw_data, aggregated_data = extract_data_for_account_lxml(root)
         # Convert raw data to a DataFrame for display
        agg_df = pd.DataFrame(aggregated_data)
        if not agg_df.empty:
            st.table(agg_df) # Display the raw data in a table format
        else:
            st.write("No Aggregated Data Found.")

if __name__ == "__main__":
    main()
