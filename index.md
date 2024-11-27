<meta http-equiv="Content-Security-Policy" content="script-src 'self' 'unsafe-eval';">

<div  id="home" style="text-align: center; font-size: 24px; margin-bottom: 10px; font-weight: bold; line-height: 1.4;">
        Benchmarking Vision-Based Object Tracking for USVs in Complex Maritime Environments
</div>
<div style="text-align: center; font-size: 16px; margin-bottom: 10px; line-height: 1.4;">
    Muhayy Ud Din, Ahsan B. Bakht, Waseem Akram, Lakmal Seneviratne, and Irfan Hussain
</div>
<div style="text-align: center;">
  {% include button.html text="GitHub" icon="github" link="https://github.com/Muhayyuddin/vision-tracking" color="#0366d6" %}
  {% include button.html text="Preprint" icon="assets/arxiv.png" link="https://arxiv.org/" color="#0366d6"  %}
  {% include button.html text="FAQs"  link="#faqs" color="#0366d6"  %}
</div>
<h5 style="margin-bottom: 10px;"> Overview </h5>
<div style="text-align: justify; font-size: 14px; margin-bottom: 10px; line-height: 1.4;">
   Vision-based target tracking is crucial for unmanned surface vehicles to perform tasks such as
inspection, monitoring, and surveillance. However, real-time tracking in complex maritime environments is
challenging due to dynamic camera movement, low visibility, and scale variation. Typically, object detection
methods combined with filtering techniques are commonly used for tracking, but they often lack robustness,
particularly in the presence of camera motion and missed detections. Although advanced tracking methods
have been proposed recently, their application in maritime scenarios is limited. To address this gap, this
study proposes a vision-guided object tracking framework for USVs, integrating state-of-the-art tracking
algorithms with low-level control systems to enable precise tracking in dynamic maritime environments.
We benchmarked the performance of seven distinct trackers, developed using advanced deep learning
techniques such as Siames Networks and Transformers, by evaluating them on both simulated and real-world
maritime datasets. In addition, we evaluated the robustness of various control algorithms in conjunction
with these tracking systems. The proposed framework was validated through simulations and real-world sea
experiments, demonstrating its effectiveness in handling dynamic maritime conditions. The results show that
SeqTrack, a Transformer-based tracker, performed best in adverse conditions, such as dust storms. Among
the control algorithms evaluated, the LQR controller demonstrated the most robust and smooth control,
allowing for stable tracking of the USV.
</div>
<h5 style="margin-bottom: 10px;">Tracking results</h5> 
<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">

  <iframe width="560" height="300" 
          src="https://www.youtube.com/embed/nt7EuF2b9zk?autoplay=1&mute=1&loop=1&playlist=nt7EuF2b9zk" 
          title="USV Tracking" frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
  </iframe>

  <iframe width="560" height="300" 
          src="https://www.youtube.com/embed/02cuiZU8Cv8?autoplay=1&mute=1&loop=1&playlist=02cuiZU8Cv8" 
          title="YouTube video player" frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
  </iframe>

</div>

<h6 style="margin-bottom: 5px;">Trackers performance</h6>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
    We evaluated the performance of the trackers under varying conditions, including clear sea environments and dust storms. The results are showcased in the videos below.
</div>
<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">

  <iframe width="560" height="300" 
          src="https://www.youtube.com/embed/6SRgelFJeew?autoplay=1&mute=1&loop=1&playlist=6SRgelFJeew" 
          title="YouTube video player" frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
  </iframe>

  <iframe width="560" height="300" 
          src="https://www.youtube.com/embed/MIL2nLxuRNs?autoplay=1&mute=1&loop=1&playlist=MIL2nLxuRNs&controls=0" 
          title="YouTube video player" frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
  </iframe>

</div>

<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
    Trackers performance on real data.
</div>
<div style="text-align: center;">
  <img src="assets/Combined_Real.png" alt="framework" />
</div>

<h5 id="framework" style="margin-bottom: 10px;">Tracking Framework</h5>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
We proposed a vision-guided object tracking framework for USVs, integrating state-of-the-art tracking
algorithms with low-level control systems to enable precise tracking in dynamic maritime environments. The framework is composed of three main modules: the Perception
module, which incorporates sensors for environmental perception and state estimation; the Guidance module, which includes a vision-based tracker and computes
guidance commands based on pixel and distance errors; and the Control module, which integrates surge and yaw control to generate tracking commands that drive
the USV’s thrusters, enabling precise target tracking.
</div>
<div style="text-align: center;">
  <img src="assets/framework-1.png" alt="framework" />
</div>

<h5 style="margin-bottom: 10px;">Controller Tunning and Performance</h5>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
    The animation below illustrates how different controllers work to minimize yaw error over time.
</div>
<div style="text-align: center;">
  <img src="assets/yaw_error_animation.gif" alt="Yaw Error Simulation" />
</div>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
    The controllers performance in thrust generation for tracking.
</div>
<div style="text-align: center;">
  <img src="assets/control.png" alt="Yaw Error Simulation" />
</div>

<h5 id="faqs" style="margin-bottom: 10px;">FAQs</h5>
<h8>Q1- Why we choose these trackers?</h8> 
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
We selected these six tracker named as, SiamFC, ATOM, DiMP, ToMP, SeqTrack, and TaMOs because they represent a range of state-of-the-art methods, from convolutional neural networks and correlation filters to advanced transformer-based models. Each tracker was chosen for its unique strengths in handling challenges like occlusion, motion blur, and dynamic background changes, which are essential for a significant performance in complex maritime environments.
</div>
<h8>Q2- Why we choose these particular Controllers?</h8> 
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
Each controller has its strengths depending on the complexity of the environment and system dynamics. We chose these controllers to capitalize on the diversity in their approaches: PID for its simplicity and ease of tuning, SMC for its robustness in handling disturbances and uncertainties, and LQR for its optimal control and smooth performance in dynamic and energy-efficient operations.
</div>
<h8>Q3- What is the benefit of this research work?</h8>
<div style="text-align: justify; font-size: 14px; line-height: 1.4;">
The benefit of this research lies in its development of a robust vision-based tracking framework tailored for Unmanned Surface Vehicles (USVs) in complex maritime environments. By integrating state-of-the-art tracking algorithms, such as Siamese Networks and Transformers, with low-level control systems, the research addresses challenges like dynamic camera movement, low visibility, and missed detections that are common in real-world sea conditions. 
</div>
