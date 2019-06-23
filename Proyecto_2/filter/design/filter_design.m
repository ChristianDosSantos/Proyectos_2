%This files calculates coefficients for a butterworth filter
%https://www.mathworks.com/help/signal/ref/butter.html#bucse3u-Wn

%Sampling freq
fs=2000;
%Cutoff freq
fc=250;
%Order of the filter
N=10;
%
Wn=fc/(fs/2);
%Coefficients
[B,A] = fir1(N,Wn)
round(B*1000)

%Graph
h = fvtool(B,A);


