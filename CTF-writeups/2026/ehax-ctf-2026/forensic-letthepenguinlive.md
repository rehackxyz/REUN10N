# forensic - let-the-penguin-live

Solved by:p5yd4wk

a stego challenge, we were provided with a video (mkv) so i simply use ffmpeg to extract contents inside
i managed to extract audio1.wav and audio2.wav
after playing around it for minutes long, i realized that we need to transform then substract to compute the difference
i use this command `sox -m audio1.wav "|sox audio2.wav -p vol -1" difference.wav`
then i put it inside sonic visualizer to inspect the spectogram

Flag:`EH4X{0n3_tr4ck_m1nd_tw0_tr4ck_f1es}`

