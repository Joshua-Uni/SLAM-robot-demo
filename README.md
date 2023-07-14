# SLAM-robot-demo

Welcome to the SLAM robot demo, an exciting showcase of how a robot can perform Simultaneous Localization and Mapping (SLAM) using the Python programming language and the Pygame module. This project provides a practical implementation of SLAM, allowing you to observe and understand the underlying principles behind this important robotic technique. By controlling a small robot in a dark room, you'll witness how it utilizes a simulated LIDAR sensor to explore and map its surroundings.

# LIDAR:
At the core of this project lies the LIDAR sensor, which simulates the functionality of a real-world LIDAR system commonly used in robotic applications. LIDAR, short for Light Detection and Ranging, employs laser beams to measure the distance between the sensor and objects in its environment. In our demonstration, the robot utilizes LIDAR-like beams to record the x and y positions of hidden walls within the dark room. This data serves as the foundation for our SLAM algorithm, enabling the robot to simultaneously map its surroundings and localize itself.

# Seed Detection:
To accurately detect and extract wall segments from the recorded LIDAR points, we employ an algorithm based on the paper titled "A line segment extraction algorithm using laser data based on seeded region growing" (DOI: 10.1177/1729881418755245). The first step of this algorithm involves identifying seed regions among the recorded points. A seed region is considered valid when the chosen points exhibit epsilon and delta errors below predefined thresholds.

The epsilon error measures the distance from each point in the seed segment to the fitted straight line obtained through the orthogonal least squares method. It ensures that the distance is within a specified threshold.

The delta error, on the other hand, quantifies the distance from each point in the seed segment to its predicted position. This prediction is derived from the intersection of the orthogonal least squares line of the potential seed region and a straight line from the sensor to the respective point. The requirement of keeping the seed-segment free from breakpoints is enforced through the delta error.

<img width="280" alt="delta" src="https://github.com/Joshua-Uni/SLAM-robot-demo/assets/112139913/6491e3f3-08a2-4314-b607-a841b6dfb4ed">

Delta Error

<img width="277" alt="seed detection" src="https://github.com/Joshua-Uni/SLAM-robot-demo/assets/112139913/d434aaa2-9490-4738-a32c-96cb515dbb36">

Seed Detection Algorithm

# Region Growing:
Once a valid seed region is identified, the algorithm proceeds with region growing, where additional points are added to the segment if they fall within the epsilon threshold. This iterative process involves recreating the orthogonal least squares line with the newly added point, continuing until points on both the left and right sides exceed the epsilon error barrier. Through this region growing technique, we effectively expand the wall segments, creating a comprehensive map of the environment.

<img width="276" alt="seed growing" src="https://github.com/Joshua-Uni/SLAM-robot-demo/assets/112139913/a7a82ad7-f181-4373-9f6f-70d3df907309">

Region Growing Algorithm

# Exploration:
As a user, you have the ability to control the movement of the small robot within the dark room. By directing the robot's path, you can witness the SLAM algorithm in action as it simultaneously explores the room, records LIDAR points, detects seed regions, and grows them into complete wall segments. This interactive exploration provides an intuitive understanding of SLAM and its potential applications in real-world robotic scenarios.

<img width="1187" alt="first" src="https://github.com/Joshua-Uni/SLAM-robot-demo/assets/112139913/290647b2-c096-4d08-a823-418beff17152">

<img width="1183" alt="second" src="https://github.com/Joshua-Uni/SLAM-robot-demo/assets/112139913/373fb121-a8d4-4302-9670-c45cfad2ac41">

<img width="1190" alt="third" src="https://github.com/Joshua-Uni/SLAM-robot-demo/assets/112139913/ec2843a2-d531-46ab-8aaa-bb4e6ddbafe7">

# Conclusion:
The SLAM Demonstration project serves as an educational and practical showcase of how robots can perform simultaneous localization and mapping. By utilizing Python and the Pygame module, we simulate a robot equipped with a LIDAR sensor, showcasing the process of exploring a dark room and creating a map of the environment. The implemented algorithm based on seeded region growing enables accurate line detection from the recorded LIDAR points. This project acts as a stepping stone for further experimentation and extension, allowing for the integration and testing of SLAM techniques on real robots. Explore, learn, and unleash the potential of SLAM with my demonstration!
