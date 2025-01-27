import streamlit as st

from ml_app import run_ml_app

def main():
    menu = ['Home', 'Predict Flight Price']
    choice = st.sidebar.radio("Menu", menu)

    if choice == 'Home':
            st.markdown(
            '''
            <h1 style='text-align: center;'> Take the Guesswork Out of Flight Planning </h1>
            <br>
            <h4 style='text-align: justify;'>Planning your next adventure or business trip?</h4>
            <p style='text-align: justify;'>We’ve got you covered! Welcome to <strong>flight price calculator</strong>! Our tool takes the guesswork out of estimating flight ticket prices. Whether you’re planning a dream vacation, a last-minute getaway, or an important business trip, we’re here to make your journey easier from the very beginning. </p>
            <br>
            <h4 style='text-align: justify;'>Our Purpose</h4>
            <p style='text-align: justify;'>We believe travel should be simple, stress-free, and budget-friendly. That’s why we’ve created this tool to help you:</p>
                <ul style='text-align: justify;'>
                    <li><strong>Plan with Confidence:</strong> Get clear flight price estimates tailored to your travel preferences.</li>
                    <li><strong>Make Smart Decisions:</strong > Avoid overspending by comparing flight options and timing your bookings wisely.</li>
                    <li><strong>Travel Anywhere:</strong> Whether it’s a quick domestic trip or an international adventure, we’re here to guide you.</li>
                    <li><strong>Save Time and Effort:</strong> Forget endless searches and complicated calculations. Our intuitive tool is designed to deliver results quickly and hassle-free.</li>
                </ul>
            </p>
            <br>
            <p style='text-align: center;'><strong>Start exploring today and let your next journey take flight with confidence!</strong></p>
            ''',
            unsafe_allow_html=True
        )
    elif choice == 'Predict Flight Price':
        run_ml_app()


if __name__ == '__main__':
    main()
