import cv2

input1="peace.jpg"
output1="resized.png"
image=cv2.imread(input1,cv2.IMREAD_UNCHANGED)
scaling_factor=int(input("Enter the scaling percentage  here : "))
new_height=int(image.shape[0]*scaling_factor/100)
new_width=int(image.shape[1]*scaling_factor/100)

output =cv2.resize(image,(new_width,new_height))
cv2.imwrite(output1,output)
cv2.waitKey(0)

