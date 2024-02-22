import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw


def main():
    st.title("Image Processing App")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # Convert image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        #  original image
        st.image(image, caption="Original Image", use_column_width=True)

        #  options
        option = st.sidebar.selectbox("Choose an option", ["Original", "Grayscale", "Binary", "Brightness & Contrast", "Symbols"])

        if option == "Original":
            st.image(image, caption="Original Image", use_column_width=True) # --> column width used to fit the image
        elif option == "Grayscale":
            grayscale_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            st.image(grayscale_image, caption="After Grayscale Image", use_column_width=True)
        elif option == "Binary":
            threshold = st.slider("Threshold", 0, 255, 128)
            threshold_y = st.slider("threshold y" , 0,255,128)
            _, binary_image = cv2.threshold(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY), threshold, threshold_y, cv2.THRESH_BINARY)

            st.image(binary_image, caption="Binary Image", use_column_width=True)
        elif option == "Brightness & Contrast":
            brightness = st.slider("Brightness", 0.0, 2.0, 1.0)
            contrast = st.slider("Contrast", 0.0, 2.0, 1.0)
            adjusted_image = cv2.convertScaleAbs(opencv_image, alpha=contrast, beta=brightness)
            st.image(adjusted_image, caption="Adjusted Image", use_column_width=True)
        elif option == "Symbols":
            draw = ImageDraw.Draw(image)
            shape = st.sidebar.selectbox("Choose a shape", ["Line", "Rectangle", "Circle", "Text"])
            
            if shape == "Line":
                start_point = tuple(st.text_input("Start Point (x, y)", value="0, 0").split(','))
                end_point = tuple(st.text_input("End Point (x, y)", value="50, 50").split(','))
                #--> line abhi choti hai to mai usko scale karunga start , max value , default value
                scale = st.slider("line scale",1,10,1)
                draw.line([int(start_point[0]), int(start_point[1]), int(end_point[0]), int(end_point[1])], fill="red", width=scale)
            elif shape == "Rectangle":
                top_left = tuple(st.text_input("Top Left (x, y)", value="0, 0").split(','))
                bottom_right = tuple(st.text_input("Bottom Right (x, y)", value="50, 50").split(','))
                 #--> line abhi choti hai to mai usko scale karunga start , max value , default value
                scale = st.slider("line scale",1,10,1)
                draw.rectangle([int(top_left[0]), int(top_left[1]), int(bottom_right[0]), int(bottom_right[1])], outline="blue", width=scale)
            elif shape == "Circle":
                center = tuple(st.text_input("Center (x, y)", value="25, 25").split(','))
                radius = st.number_input("Radius", min_value=1, value=10)
                 #--> line abhi choti hai to mai usko scale karunga start , max value , default value
                scale = st.slider("line scale",1,10,1)
                draw.ellipse([int(center[0]) - radius, int(center[1]) - radius, int(center[0]) + radius, int(center[1]) + radius], outline="green", width=scale)
            elif shape == "Text":
                image_np = np.array(image)
                text = st.text_input("Enter text", "Hello, Streamlit!")
                position = tuple(map(int, st.text_input("Position (x, y)", value="10, 10").split(',')))
                scale = st.slider("Text scale", 1, 20, 1)  # Increased the range for larger font sizes
                cv2.putText(image_np, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 0, 255), thickness=2)
                image = Image.fromarray(image_np)
                
            st.image(image, caption='Symbols', use_column_width=True)
if __name__ == "__main__":
    main()
